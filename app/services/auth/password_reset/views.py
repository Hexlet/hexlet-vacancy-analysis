import logging
from datetime import datetime, timedelta
from typing import Any

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views import View
from django_ratelimit.decorators import ratelimit  # type: ignore
from inertia import InertiaResponse, location  # type: ignore
from inertia import render as inertia_render

from . import configs
from .models import PasswordResetToken
from .tasks import send_mail_task

User = get_user_model()
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

    subject_template_name = "Password reset"  # Шаблон темы письма
    email_template_name = "password_reset_email.html"  # Шаблон тела письма
    from_email = settings.DEFAULT_FROM_EMAIL  # Email-адрес отправителя
    token_generator = PasswordResetTokenGenerator()  # Генератор токенов

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

        email: str | None = request.POST.get("email")
        if not email:
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
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            logger.error("email does not belong to any user")
            user = None

        if user:
            with transaction.atomic():
                # Удаление старых токенов пользователя
                PasswordResetToken.mark_all_as_used(user)

                # Генерация нового токена и расчет времени истечения
                token: str = self.token_generator.make_token(user)
                current_time: datetime = timezone.now()
                time_out: timedelta = timedelta(configs.PASSWORD_RESET_TIMEOUT)
                expires_at: datetime = current_time + time_out

                # Формирование ссылки для сброса пароля
                reset_url: str = request.build_absolute_uri(
                    reverse("password_reset_redirect") + f"?token={token}"
                )

                # Отправка email и сохранение токена
                self.send_reset_email(email, reset_url)
                PasswordResetToken.objects.create(
                    user_id=user,
                    token_hash=hash(token),
                    expires_at=expires_at,
                )

        return inertia_render(
            request,
            "PasswordResetCompletePage",
            props={"status": "ok", "status_code": 200},
        )

    def send_reset_email(self, email: str, reset_url: str) -> None:
        """
        Отправляет email с ссылкой для сброса пароля.

        Args:
            email (str): Адрес электронной почты получателя.
            reset_url (str): Ссылка для сброса пароля.
        """
        subject: str = self.subject_template_name
        html_message: str = render_to_string(
            self.email_template_name,
            {
                "email": email,
                "reset_url": reset_url,
            },
        )
        plain_message: str = strip_tags(html_message)

        send_mail_task.delay(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=self.from_email,
            recipient_list=[email],
            fail_silently=False,
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
        # Поиск неиспользованного токена по хэшу
        reset_token = PasswordResetToken.objects.filter(
            token_hash=hash(token), is_used=False
        ).first()

        if reset_token:
            # Проверка срока действия токена
            if reset_token.expires_at > timezone.now():
                return inertia_render(
                    request,
                    "PasswordResetConfirmPage",
                    props={
                        "status": "ok",
                        "status_code": 200,
                        "data": {"token": token},
                    },
                )

        logger.error("Token is expired or invalid")
        return inertia_render(
            request,
            "ErrorPage",
            props={
                "status": "Bad Request",
                "status_code": 400,
                "message": "Ссылка недействительна или истекла",
            },
        )

    def post(self, request: HttpRequest) -> InertiaResponse:
        """
        Обрабатывает POST-запрос для сброса пароля.

        Args:
            request (HttpRequest): Объект HTTP-запроса, содержащий:
                - 'token': Хэш токена из URL.
                - 'newPassword': Новый пароль пользователя.

        Returns:
            HttpResponse:
                - При успешном сбросе: главная страница.
                - При ошибках: страница подтверждения с ошибкой 422 или
                  страница ошибки с кодом 400.
        """
        token: str | None = request.POST.get("token")
        new_password: str | None = request.POST.get("newPassword")

        if not token or not new_password:
            return inertia_render(
                request,
                "ErrorPage",
                props={
                    "status": "Bad Request",
                    "status_code": 400,
                },
            )

        # Валидация сложности пароля
        try:
            validate_password(new_password)
        except ValidationError:
            return inertia_render(
                request,
                "PasswordResetConfirmPage",
                props={
                    "status": "Unprocessable Entity",
                    "status_code": 422,
                    "message": "Слабый пароль",
                    "data": {"token": token},
                },
            )

        # Поиск активного токена
        reset_token: PasswordResetToken | None = PasswordResetToken.objects.filter(
            token_hash=token, is_used=False
        ).first()

        if reset_token:
            if reset_token.expires_at > timezone.now():
                user = User.objects.get(id=reset_token.user_id.pk)
                user.set_password(new_password)
                user.save()
                reset_token.mark_as_used()
                return inertia_render(
                    request,
                    "HomePage",
                    props={"status": "ok", "status_code": 200},
                )

        return inertia_render(
            request,
            "ErrorPage",
            props={
                "status": "Bad Request",
                "status_code": 400,
                "message": "Недействительный токен",
            },
        )
