import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from app.services.auth.users.models import UserIdentity

User = get_user_model()


class GithubBackend(BaseBackend):
    """
    Ауф через GitHub:
    - Обменивает code на токен
    - Получает user info
    - Создаёт или возвращает User
    """

    def authenticate(self, request, code=None, **kwargs):
        if code is None:
            return None
        # обмен code -> token
        token = self._exchange_code_for_token(code)
        if not token:
            return None

        # запрос профиля
        info = self._fetch_user_info(token)
        if not info:
            return None

        # устойчивый id пользователя GitHub
        provider_user_id = str(info.get("id") or "")
        if not provider_user_id:
            return None

        # если identity уже есть — возвращаем связанного пользователя
        identity = (
            UserIdentity.objects.select_related("user")
            .filter(provider="github", provider_user_id=provider_user_id)
            .first()
        )
        if identity:
            user = identity.user
        else:
            link_to_user = kwargs.get("link_to_user")
            if link_to_user is not None:
                user = link_to_user
            else:
                # email может быть скрыт в профиле -> пытаемся получить из /user/emails
                email = self._resolve_email(token, info)
                if not email:
                    return None
                first_name, last_name = self._split_name(info)
                defaults = {
                    "first_name": first_name or "",
                    "last_name": last_name or "",
                }
                user, _ = User.objects.get_or_create(email=email, defaults=defaults)

            # создать identity
            email_for_identity = None
            if "email" in info and info.get("email"):
                email_for_identity = info.get("email")
            else:
                # из /user/emails могли выбрать
                try:
                    email_for_identity = email  # type: ignore[name-defined]
                except NameError:
                    email_for_identity = None
            UserIdentity.objects.create(
                user=user,
                provider="github",
                provider_user_id=provider_user_id,
                email=email_for_identity,
                email_verified=bool(email_for_identity),
                profile=info,
            )

        # подсказка для обновления ФИО
        if request is not None:
            first_name, last_name = self._split_name(info)
            request.session["github_profile_suggested"] = {
                "first_name": first_name or "",
                "last_name": last_name or "",
            }
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    # helpers

    def _exchange_code_for_token(self, code):
        try:
            res = requests.post(
                "https://github.com/login/oauth/access_token",
                headers={"Accept": "application/json"},
                data={
                    "client_id": settings.GITHUB_CLIENT_ID,
                    "client_secret": settings.GITHUB_CLIENT_SECRET,
                    "code": code,
                    "redirect_uri": settings.GITHUB_REDIRECT_URI,
                },
            )
            res.raise_for_status()
            return res.json().get("access_token")
        except requests.RequestException:
            return None

    def _fetch_user_info(self, token):
        try:
            info_res = requests.get(
                "https://api.github.com/user",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {token}",
                },
            )
            info_res.raise_for_status()
            return info_res.json()
        except requests.RequestException:
            return None

    def _resolve_email(self, token, info):
        email = info.get("email")
        if email:
            return email
        try:
            emails_res = requests.get(
                "https://api.github.com/user/emails",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {token}",
                },
            )
            emails_res.raise_for_status()
            emails = emails_res.json() or []
            return next(
                (e["email"] for e in emails if e.get("primary") and e.get("verified")),
                None,
            ) or next(
                (e["email"] for e in emails if e.get("verified")),
                None,
            )
        except requests.RequestException:
            return None

    def _split_name(self, info):
        full_name = (info.get("name") or "").strip()
        if full_name:
            first_name, _, last_name = full_name.partition(" ")
        else:
            first_name, last_name = (info.get("login") or ""), ""
        return first_name, last_name

    def _update_user_names_if_needed(self, user, created, defaults):
        first_name = defaults["first_name"]
        last_name = defaults["last_name"]
        updated = False
        if not created:
            if (
                hasattr(user, "first_name")
                and first_name
                and user.first_name != first_name
            ):
                user.first_name = first_name
                updated = True
            if hasattr(user, "last_name") and last_name and user.last_name != last_name:
                user.last_name = last_name
                updated = True
            if updated:
                fields = []
                if hasattr(user, "first_name"):
                    fields.append("first_name")
                if hasattr(user, "last_name"):
                    fields.append("last_name")
                user.save(update_fields=fields or None)
