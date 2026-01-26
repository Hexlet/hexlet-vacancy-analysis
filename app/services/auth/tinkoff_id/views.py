import base64
import logging
import secrets
from typing import Any
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.models import AbstractBaseUser
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.views import View
from inertia import render as inertia_render  # type: ignore

logger = logging.getLogger(__name__)
User = get_user_model()


class TinkoffLogin(View):
    """Инициирует OAuth-процесс авторизации через Tinkoff ID.

    Генерирует безопасный случайный токен состояния, сохраняет контекст
    предыдущей страницы и формирует URL для перенаправления пользователя
    на страницу авторизации Tinkoff.
    """

    def get(self, request: HttpRequest) -> HttpResponseRedirect:
        """Обрабатывает GET-запрос для инициации авторизации.

        Args:
            request: Объект HTTP-запроса от Django.

        Returns:
            Перенаправление на URL авторизации Tinkoff.
        """
        state: str = secrets.token_urlsafe(32)
        request.session["state"] = state

        previous_page: str | None = request.META.get("HTTP_REFERER")
        request.session["previous_page"] = previous_page

        params: dict[str, str] = {
            "client_id": settings.TINKOFF_ID_CLIENT_ID,
            "redirect_uri": settings.TINKOFF_ID_REDIRECT_URI,
            "state": state,
            "response_type": "code",
            "scope": ",".join(settings.TINKOFF_ID_SCOPE),
        }

        auth_url: str = f"{settings.TINKOFF_ID_AUTH_URL}?{urlencode(params)}"
        return redirect(auth_url)


class TinkoffCallback(View):
    """Обрабатывает callback OAuth-процесса авторизации через Tinkoff ID.

    Выполняет валидацию состояния, получение токена, проверку области действия,
    получение информации о пользователе и авторизацию/регистрацию.
    """

    error_page: str = "ErrorPage"

    def get(self, request: HttpRequest) -> HttpResponse:
        """Обрабатывает GET-запрос после возврата с Tinkoff ID.

        Args:
            request: Объект HTTP-запроса от Django.

        Returns:
            Перенаправление на предыдущую страницу или страницу ошибки.
        """
        previous_page: str | None = request.session.pop("previous_page", "/")

        # Валидация state
        if not self._validate_state(request):
            return self._handle_error("Invalid state parameter", 403)

        # Получение кода авторизации
        code: str | None = request.GET.get("code")
        if not code:
            return self._handle_error("Missing code parameter", 403)

        # Получение access-токена
        token_response: dict[str, Any] | None = self._get_access_token(code)
        if not token_response:
            return self._handle_error("Failed to get access token", 403)

        access_token: str | None = token_response.get("access_token")
        if not access_token:
            return self._handle_error("Missing access token in response", 403)

        # Проверка области действия токена
        if not self._validate_token_scope(access_token):
            return self._handle_error("Missing required scope", 403)

        # Получение информации о пользователе
        user_info: dict[str, Any] | None = self._get_user_info(access_token)
        if not user_info:
            return self._handle_error("Failed to get user info", 403)

        email: str | None = user_info.get("email")
        if not email:
            return self._handle_error("User has no email", 403)

        # Авторизация или регистрация пользователя
        self._authenticate_user(request, email)
        return redirect(previous_page or "/")

    def _validate_state(self, request: HttpRequest) -> bool:
        """Проверяет валидность CSRF-токена состояния.

        Args:
            request: Объект HTTP-запроса от Django.

        Returns:
            True если state валидна, иначе False.
        """
        state: str | None = request.GET.get("state")
        session_state: str | None = request.session.pop("state", None)
        return state is not None and state == session_state

    def _get_access_token(self, code: str) -> dict[str, Any] | None:
        """Получает access-токен по коду авторизации.

        Args:
            code: Код авторизации от Tinkoff.

        Returns:
            Словарь с токеном или None при ошибке.
        """
        token_data: dict[str, str] = {
            "grant_type": "authorization_code",
            "redirect_uri": settings.TINKOFF_ID_REDIRECT_URI,
            "code": code,
        }
        return self._make_oauth_request(
            settings.TINKOFF_ID_TOKEN_URL,
            data=token_data,
        )

    def _validate_token_scope(self, access_token: str) -> bool:
        """Проверяет, содержит ли токен необходимые области доступа.

        Args:
            access_token: Access-токен для проверки.

        Returns:
            True если все требуемые области присутствуют, иначе False.
        """
        introspect_data: dict[str, str] = {
            "token": access_token,
        }
        introspect_response: dict[str, Any] | None = self._make_oauth_request(
            settings.TINKOFF_ID_INTROSPECT_URL,
            data=introspect_data,
        )
        if not introspect_response:
            return False

        granted_scope: set[str] = set(introspect_response.get("scope", "").split())
        required_scope: set[str] = set(settings.TINKOFF_ID_SCOPE)
        return required_scope.issubset(granted_scope)

    def _get_user_info(self, access_token: str) -> dict[str, Any] | None:
        """Получает информацию о пользователе используя access-токен.

        Args:
            access_token: Access-токен для запроса информации.

        Returns:
            Словарь с информацией пользователя или None при ошибке.
        """
        user_data: dict[str, str] = {
            "client_id": settings.TINKOFF_ID_CLIENT_ID,
            "client_secret": settings.TINKOFF_ID_CLIENT_SECRET,
        }
        return self._make_oauth_request(
            settings.TINKOFF_ID_USERINFO_URL,
            data=user_data,
            auth_type="Bearer",
            token=access_token,
        )

    def _authenticate_user(self, request: HttpRequest, email: str) -> None:
        """Авторизует существующего пользователя или создаёт нового.

        Args:
            request: Объект HTTP-запроса от Django.
            email: Email адрес пользователя.
        """
        user: AbstractBaseUser
        created: bool
        user, created = User.objects.get_or_create(email=email)

        action: str = (
            "Create new user account" if created else "User account already exists"
        )
        logger.info(f"{action}")

        login(request, user, backend="django.contrib.auth.backends.ModelBackend")

    def _create_basic_auth_header(self) -> str:
        """Генерирует заголовок Basic Authentication для OAuth-запросов.

        Returns:
            Строка заголовка формата 'Basic <base64_кодированные_учетные_данные>'.
        """
        credentials_str: str = (
            f"{settings.TINKOFF_ID_CLIENT_ID}:{settings.TINKOFF_ID_CLIENT_SECRET}"
        )
        credentials_b64: str = base64.b64encode(credentials_str.encode("utf-8")).decode(
            "utf-8"
        )
        return f"Basic {credentials_b64}"

    def _make_oauth_request(
        self,
        url: str,
        data: dict[str, str],
        auth_type: str = "Basic",
        token: str | None = None,
    ) -> dict[str, Any] | None:
        """Выполняет HTTP POST-запрос к OAuth-эндпоинту.

        Args:
            url: Адрес API для отправки запроса.
            data: Данные запроса (формат x-www-form-urlencoded).
            auth_type: Тип авторизации ("Basic" или "Bearer"). По умолчанию "Basic".
            token: Токен для Bearer-авторизации.
                   Используется только если auth_type="Bearer".

        Returns:
            JSON-ответ сервера или None при ошибке.

        Exceptions:
            Не выбрасывает исключения, логирует ошибки при неудачном запросе.
        """
        authorization_value: str = (
            f"{auth_type} {token}" if token else self._create_basic_auth_header()
        )
        headers: dict[str, str] = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": authorization_value,
        }

        try:
            response: requests.Response = requests.post(
                url, headers=headers, data=data, timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            logger.error(
                f"OAuth request to {url} failed: {exc}",
                exc_info=True,
            )
            return None

    def _handle_error(self, message: str, status_code: int) -> HttpResponse:
        """Обрабатывает ошибки OAuth-процесса.

        Args:
            message: Сообщение об ошибке.
            status_code: HTTP-код ошибки.

        Returns:
            HTTP-ответ с шаблоном страницы ошибки.
        """
        logger.error(message)
        return inertia_render(
            self.request,
            self.error_page,
            props={"message": message, "status_code": status_code},
        )
