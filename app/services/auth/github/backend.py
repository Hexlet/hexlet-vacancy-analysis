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
        # игнорируем вызовы не для этого провайдера
        if kwargs.get("provider") not in ("github", None):
            return None
        if code is None:
            return None
        token = self._exchange_code_for_token(code)
        if not token:
            return None

        info = self._fetch_user_info(token)
        if not info:
            return None

        provider_user_id = self._get_provider_user_id(info)
        identity = self._get_identity(provider_user_id) if provider_user_id else None
        if identity:
            user = identity.user
        else:
            link_to_user = kwargs.get("link_to_user")
            user, email_for_identity = self._resolve_user_for_auth(
                request, info, token, link_to_user
            )
            if user is None:
                return None
            if provider_user_id:
                self._ensure_identity(user, provider_user_id, info, email_for_identity)

        self._store_suggested_names(request, info)
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

    def _get_provider_user_id(self, info):
        return str(info.get("id") or "")

    def _get_identity(self, provider_user_id):
        return (
            UserIdentity.objects.select_related("user")
            .filter(provider="github", provider_user_id=provider_user_id)
            .first()
        )

    def _resolve_user_for_auth(self, request, info, token, link_to_user):
        if link_to_user is not None:
            email_for_identity = info.get("email") or self._resolve_email(token, info)
            return link_to_user, email_for_identity

        email = self._resolve_email(token, info)
        if not email:
            return None, None
        first_name, last_name = self._split_name(info)
        defaults = {"first_name": first_name or "", "last_name": last_name or ""}
        user, _ = User.objects.get_or_create(email=email, defaults=defaults)
        return user, email

    def _ensure_identity(self, user, provider_user_id, info, email_for_identity):
        UserIdentity.objects.create(
            user=user,
            provider="github",
            provider_user_id=provider_user_id,
            email=email_for_identity,
            email_verified=bool(email_for_identity),
            profile=info,
        )

    def _store_suggested_names(self, request, info):
        if request is None:
            return
        first_name, last_name = self._split_name(info)
        request.session["github_profile_suggested"] = {
            "first_name": first_name or "",
            "last_name": last_name or "",
        }
