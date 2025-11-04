import base64
import logging
import secrets
from urllib.parse import urlencode

import requests
from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect
from django.views import View
from inertia import render as inertia_render

logger = logging.getLogger(__name__)
User = get_user_model()


class TinkoffLogin(View):
    """
    Класс обработки запроса авторизации через Tinkoff ID.

    Реализует начальный этап OAuth-процесса: генерирует уникальный
    идентификатор состояния (state), сохраняет контекст предыдущей
    страницы и формирует URL для перенаправления пользователя на страницу
    авторизации Tinkoff.
    """

    def get(self, request):
        """
        Обрабатывает GET-запрос для инициации авторизации.

        Генерирует безопасный случайный токен `state`, сохраняет его в сессии,
        записывает адрес предыдущей страницы из заголовка HTTP_REFERER и формирует
        URL для авторизации с необходимыми параметрами.

        Args:
            request (HttpRequest): Объект HTTP-запроса от Django.

        Returns:
            HttpResponseRedirect: Перенаправление на URL авторизации Tinkoff.
        """
        # Генерация уникального токена состояния для предотвращения CSRF-атак
        state = secrets.token_urlsafe(32)
        request.session["state"] = state

        # Сохранение адреса, с которого был выполнен переход
        previous_page = request.META.get("HTTP_REFERER")
        request.session["previous_page"] = previous_page

        # Формирование параметров запроса авторизации
        params = {
            "client_id": settings.TINKOFF_ID_CLIENT_ID,
            "redirect_uri": settings.TINKOFF_ID_REDIRECT_URI,
            "state": state,
            "response_type": "code",
            "scope": ",".join(settings.TINKOFF_ID_SCOPE),
        }

        # Формирование финального URL для перенаправления пользователя
        auth_url = f"{settings.TINKOFF_ID_AUTH_URL}?{urlencode(params)}"
        return redirect(auth_url)


class TinkoffCallback(View):
    """
    Класс обработки обратного вызова (callback) OAuth-процесса
    авторизации через Tinkoff ID.

    Выполняет следующие задачи:
    - Проверку безопасности запроса (валидация `state`).
    - Получение access-токена по авторизационному коду.
    - Проверку области действия токена.
    - Получение информации о пользователе.
    - Авторизацию или регистрацию пользователя в системе.
    """

    error_page = "ErrorPage"  # Шаблон страницы ошибки

    def _create_basic_auth_header(self):
        """
        Генерирует заголовок Basic Authentication для OAuth-запросов.

        Формирует строку вида "Basic <base64_кодированные_учетные_данные>".

        Returns:
            str: Строка заголовка Basic Authentication.
        """
        credentials = (
            base64.encodebytes(
                (
                    "%s:%s"
                    % (
                        settings.TINKOFF_ID_CLIENT_ID,
                        settings.TINKOFF_ID_CLIENT_SECRET,
                    )
                ).encode("utf8")
            )
            .decode("utf8")
            .replace("\n", "")
        )
        return f"Basic {credentials}"

    def _make_oauth_request(self, url, data, auth_type="Basic", token=None):
        """
        Выполняет HTTP POST-запрос к OAuth-эндпоинту.

        Args:
            url (str): Адрес API для отправки запроса.
            data (dict): Данные запроса (формат x-www-form-urlencoded).
            auth_type (str): Тип авторизации ("Basic" или "Bearer").
            token (str, optional): Токен для Bearer-авторизации.

        Returns:
            dict or None: JSON-ответ сервера или None при ошибке.
        """
        headers = {
            "content_type": "application/x-www-form-urlencoded",
            "Authorization": (
                f"{auth_type} {token}" if token else self._create_basic_auth_header()
            ),
        }
        response = requests.post(url, headers=headers, data=data)
        if response.status_code != 200:
            logger.error(f"Request failed to {url}: {response.status_code}")
            return None
        return response.json()

    def get(self, request):
        """
        Обрабатывает GET-запрос после возврата пользователя с Tinkoff ID.

        Выполняет полный цикл OAuth-авторизации:
        1. Проверяет корректность `state`.
        2. Получает access-токен.
        3. Проверяет область действия токена.
        4. Получает информацию о пользователе.
        5. Авторизует или регистрирует пользователя.

        Args:
            request (HttpRequest): Объект HTTP-запроса от Django.

        Returns:
            HttpResponseRedirect: Перенаправление на предыдущую страницу
                                  или страницу ошибки.
        """
        previous_page = request.session.pop("previous_page", "/")

        state = request.GET.get("state")
        if state != request.session.pop("state"):
            return self._handle_error("Invalid state parameter", 403)

        code = request.GET.get("code")
        if not code:
            return self._handle_error("Missing code parameter", 403)

        token_data = {
            "grant_type": "authorization_code",
            "redirect_uri": settings.TINKOFF_ID_REDIRECT_URI,
            "code": code,
        }
        token_response = self._make_oauth_request(
            settings.TINKOFF_ID_TOKEN_URL, data=token_data
        )
        if not token_response:
            return self._handle_error("Failed to get access token", 403)

        access_token = token_response.get("access_token")

        introspect_data = {
            "token": access_token,
        }
        introspect_response = self._make_oauth_request(
            settings.TINKOFF_ID_INTROSPECT_URL,
            data=introspect_data,
        )
        if not introspect_response:
            return self._handle_error("Failed to get introspect token", 403)

        granted_scope = set(introspect_response.get("scope", ""))
        required_scope = set(settings.TINKOFF_ID_SCOPE)
        if not required_scope.issubset(granted_scope):
            return self._handle_error("Missing scope", 403)

        user_data = {
            "client_id": settings.TINKOFF_ID_CLIENT_ID,
            "client_secret": settings.TINKOFF_ID_CLIENT_SECRET,
        }
        user_info = self._make_oauth_request(
            settings.TINKOFF_ID_USERINFO_URL,
            data=user_data,
            auth_type="Bearer",
            token=access_token,
        )
        if not user_info:
            return self._handle_error("Failed to get user info", 403)

        email = user_info.get("email")
        if not email:
            return self._handle_error("User has no email", 403)

        user, created = User.objects.get_or_create(email=email)
        if created:
            logger.info(f"Create new user account for: [{email}]")
        else:
            logger.info(f"User account already exists for: [{email}]")

        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect(previous_page)

    def _handle_error(self, message, status_code):
        """
        Обрабатывает ошибки OAuth-процесса.

        Логгирует ошибку и возвращает шаблон страницы ошибки.

        Args:
            message (str): Сообщение об ошибке.
            status_code (int): Код HTTP-ошибки.

        Returns:
            HttpResponse: Ответ с шаблоном страницы ошибки.
        """
        logger.error(message)
        return inertia_render(
            self.request,
            self.error_page,
            props={"message": message, "status_code": status_code},
        )
