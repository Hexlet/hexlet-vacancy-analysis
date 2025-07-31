import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

User = get_user_model()


class YandexBackend(BaseBackend):
    """
    Ауф через Яндекс:
    - Обменивает code на токен
    - Получает user info
    - Создаёт или возвращает User
    """

    def authenticate(self, request, code=None, **kwargs):
        if code is None:
            return None
        # обмен code -> token
        res = requests.post(
            "https://oauth.yandex.ru/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.YANDEX_CLIENT_ID,
                "client_secret": settings.YANDEX_CLIENT_SECRET,
            },
        )
        try:
            res.raise_for_status()
        except requests.RequestException:
            return None
        token = res.json().get("access_token")
        if not token:
            return None

        # запрос профиля
        info_res = requests.get(
            "https://login.yandex.ru/info",
            params={"format": "json"},
            headers={"Authorization": f"OAuth {token}"},
        )
        try:
            info_res.raise_for_status()
        except requests.RequestException:
            return None
        info = info_res.json()
        email = info.get("default_email")
        if not email:
            return None

        # создать/обновить user
        defaults = {
            "first_name": info.get("first_name", ""),
            "last_name": info.get("last_name", ""),
        }
        user, _ = User.objects.get_or_create(email=email, defaults=defaults)
        # можно обновить имя/фамилию
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
