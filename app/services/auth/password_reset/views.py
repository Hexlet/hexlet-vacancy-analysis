import logging
from typing import Any

from django.http import HttpRequest
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django_ratelimit.decorators import ratelimit  # type: ignore
from inertia import InertiaResponse, location  # type: ignore
from inertia import render as inertia_render

from .forms import PasswordResetConfirmForm, PasswordResetForm
from .services.exceptions import InvalidToken, ResetException
from .services.password_reset import PasswordResetService
from .services.password_reset_confirm import ConfirmPasswordResetService

logger = logging.getLogger(__name__)


class PasswordResetView(View):
    """
    Класс обработки запросов на сброс пароля.

    Реализует функциональность:
    - Отображение формы сброса пароля (GET-запрос).
    - Обработка отправки email для сброса пароля (POST-запрос).
    - Генерация токена и отправка ссылки на сброс.
    - Ограничение частоты запросов через декораторы.
    """

    service: PasswordResetService = PasswordResetService()

    def get(self, request: HttpRequest) -> InertiaResponse:
        """
        Обрабатывает GET-запрос для отображения страницы сброса пароля.

        Args:
            request (HttpRequest): Объект HTTP-запроса от Django.

        Returns:
            HttpResponse: Ответ с шаблоном страницы сброса пароля.
        """
        logger.info("Password reset service started")
        return inertia_render(
            request,
            "PasswordResetPage",
            props={"status": "ok", "status_code": 200},
        )

    # Лимит по IP: 3 запроса в час
    @method_decorator(ratelimit(key="ip", rate="3/h"))
    # Лимит по email: 3 запроса в час
    @method_decorator(ratelimit(key="post:email", rate="3/h"))
    def post(self, request: HttpRequest) -> InertiaResponse:
        """
        Обрабатывает POST-запрос для инициации сброса пароля.

        Выполняет следующие шаги:
        1. Проверяет достижение лимита запросов.
        2. Валидирует наличие email в данных запроса.
        3. Поиск пользователя по email.
        4. Генерация уникального токена и создание ссылки для сброса.
        5. Отправка email с инструкциями.

        Args:
            request (HttpRequest): Объект HTTP-запроса от Django.

        Returns:
            HttpResponse: Ответ с результатом операции или ошибкой.
        """
        was_limited: Any | bool = getattr(request, "limited", False)
        logger.info(f"Limit reached: [{was_limited}]")

        if was_limited:
            return inertia_render(
                request,
                "ErrorPage",
                props={
                    "message": "Too many requests. Try again later.",
                    "status_code": 429,
                },
            )

        form = PasswordResetForm(request.POST)
        if not form.is_valid():
            return inertia_render(
                request,
                "ErrorPage",
                props={
                    "status": "Unprocessable Entity",
                    "status_code": 422,
                    "message": "Email is required",
                },
            )
        try:
            self.service.request_reset(
                email=form.cleaned_data["email"],
                request=request,
            )
        except ResetException:
            logger.info("Password reset requested for unknown email")

        return inertia_render(
            request,
            "PasswordResetCompletePage",
            props={"status": "ok", "status_code": 200},
        )


def redirect_mail_link(request: HttpRequest) -> InertiaResponse:
    """
    Обрабатывает запрос на перенаправление к странице подтверждения сброса
    пароля.

    Извлекает токен из GET-параметров запроса, формирует URL для страницы
    подтверждения и выполняет редирект на этот адрес.

    Args:Task
        request (HttpRequest): Объект HTTP-запроса,
                               содержащий GET-параметр 'token'.

    Returns:
        HttpResponseRedirect: Перенаправление на страницу подтверждения сброса
                    пароля с переданным токеном в качестве параметра запроса.
    """
    token: str | None = request.GET.get("token")
    if not token:
        return inertia_render(
            request,
            "ErrorPage",
            props={
                "status": "Bad Request",
                "status_code": 400,
            },
        )
    url: str = reverse("password_reset_confirm") + f"?token={token}"
    return location(url)


class PasswordResetConfirmView(View):
    """
    Класс обработки подтверждения сброса пароля.

    Реализует следующие функции:
    - Проверку валидности токена сброса пароля (GET-запрос).
    - Обновление пароля пользователя и отмечание токена как использованного
      (POST-запрос).
    - Валидацию нового пароля перед сохранением.
    """

    service = ConfirmPasswordResetService()

    def get(self, request: HttpRequest) -> InertiaResponse:
        """
        Обрабатывает GET-запрос для проверки действительности токена.

        Args:
            request (HttpRequest): Объект HTTP-запроса, содержащий параметр
                                   'token' в URL.

        Returns:
            HttpResponse:
                - Если токен действителен: страница подтверждения сброса
                  пароля.
                - Если токен недействителен или истёк: страница ошибки с
                  кодом 400.
        """
        token: str | None = request.GET.get("token")
        if not token or not self.service.is_valid(token=token):
            logger.error("Token is expired or invalid")
            return inertia_render(
                request,
                "ErrorPage",
                props={
                    "status": "Bad Request",
                    "status_code": 400,
                    "message": "Invalid or expired link",
                },
            )
        return inertia_render(
            request,
            "PasswordResetConfirmPage",
            props={
                "status": "ok",
                "status_code": 200,
                "data": {"token": token},
            },
        )

    def post(self, request: HttpRequest) -> InertiaResponse:
        """
        Обрабатывает POST-запрос для сброса пароля.

        Args:
            request (HttpRequest): Объект HTTP-запроса, содержащий:
                - 'token': Хэш токена из URL.
                - 'new_password': Новый пароль пользователя.

        Returns:
            HttpResponse:
                - При успешном сбросе: главная страница.
                - При ошибках: страница подтверждения с ошибкой 422 или
                  страница ошибки с кодом 400.
        """
        form = PasswordResetConfirmForm(request.POST)

        if not form.is_valid():
            return inertia_render(
                request,
                "ErrorPage",
                props={
                    "status": "Bad Request",
                    "status_code": 400,
                },
            )

        try:
            self.service.confirm(
                token=form.cleaned_data["token"],
                new_password=form.cleaned_data["new_password"],
            )
        except InvalidToken:
            return inertia_render(
                request,
                "PasswordResetConfirmPage",
                props={
                    "status": "Unprocessable Entity",
                    "status_code": 422,
                    "message": "Слабый пароль",
                },
            )

        return inertia_render(
            request,
            "HomePage",
            props={"status": "ok", "status_code": 200},
        )
