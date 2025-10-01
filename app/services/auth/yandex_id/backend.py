import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from app.services.auth.users.models import UserIdentity

User = get_user_model()


class YandexBackend(BaseBackend):
    """
    Ауф через Яндекс:
    - Обменивает code на токен
    - Получает user info
    - Создаёт или возвращает User
    """

    def authenticate(self, request, code=None, **kwargs):
        # игнорируем вызовы не для этого провайдера
        if kwargs.get("provider") not in ("yandex", None):
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
            user, email_for_identity = self._resolve_user_for_auth(info, link_to_user)
            if user is None:
                return None
            if provider_user_id:
                self._ensure_identity(user, provider_user_id, info, email_for_identity)

        self._store_suggested_names(request, info)
        return user

    # --- helpers ---
    def _exchange_code_for_token(self, code):
        try:
            res = requests.post(
                "https://oauth.yandex.ru/token",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": settings.YANDEX_CLIENT_ID,
                    "client_secret": settings.YANDEX_CLIENT_SECRET,
                },
            )
            res.raise_for_status()
            return res.json().get("access_token")
        except requests.RequestException:
            return None

    def _fetch_user_info(self, token):
        try:
            info_res = requests.get(
                "https://login.yandex.ru/info",
                params={"format": "json"},
                headers={"Authorization": f"OAuth {token}"},
            )
            info_res.raise_for_status()
            return info_res.json()
        except requests.RequestException:
            return None

    def _get_provider_user_id(self, info):
        return str(
            info.get("id") or info.get("psuid") or info.get("default_email") or ""
        )

    def _get_identity(self, provider_user_id):
        return (
            UserIdentity.objects.select_related("user")
            .filter(provider="yandex", provider_user_id=provider_user_id)
            .first()
        )

    def _resolve_user_for_auth(self, info, link_to_user):
        if link_to_user is not None:
            return link_to_user, info.get("default_email")

        email = info.get("default_email")
        if not email:
            return None, None
        defaults = {
            "first_name": info.get("first_name", ""),
            "last_name": info.get("last_name", ""),
        }
        user, _ = User.objects.get_or_create(email=email, defaults=defaults)
        return user, email

    def _ensure_identity(self, user, provider_user_id, info, email_for_identity):
        UserIdentity.objects.create(
            user=user,
            provider="yandex",
            provider_user_id=provider_user_id,
            email=email_for_identity,
            email_verified=bool(email_for_identity),
            profile=info,
        )

    def _store_suggested_names(self, request, info):
        if request is None:
            return
        suggest = {
            "first_name": info.get("first_name", ""),
            "last_name": info.get("last_name", ""),
        }
        request.session["yandex_profile_suggested"] = suggest

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
