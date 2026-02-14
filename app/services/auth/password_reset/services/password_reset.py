from datetime import timedelta

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import transaction
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags

from app.services.auth.users.models import User

from ..models import PasswordResetToken
from ..tasks import send_mail_task
from ..utils import hash_token
from .exceptions import ResetException


class PasswordResetService:
    subject_template_name: str = "Password reset"
    email_template_name: str = "password_reset_email.html"
    from_email: str = settings.EMAIL_FOR_PASSWORD_RESET
    token_generator: PasswordResetTokenGenerator = PasswordResetTokenGenerator()

    def request_reset(self, *, email: str, request: HttpRequest) -> None:
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ResetException

        self.create_and_send(
            user=user,
            email=email,
            request=request,
        )

    @transaction.atomic
    def create_and_send(self, *, user: User, email: str, request: HttpRequest) -> None:
        PasswordResetToken.mark_all_as_used(user)

        token = self.token_generator.make_token(user)
        expires_at = timezone.now() + timedelta(
            seconds=int(settings.PASSWORD_RESET_TIMEOUT)
        )

        reset_url = request.build_absolute_uri(
            reverse("password_reset_redirect") + f"?token={token}"
        )

        self.send_reset_email(email, reset_url)
        PasswordResetToken.objects.create(
            user=user,
            token_hash=hash_token(token),
            expires_at=expires_at,
        )

    def send_reset_email(self, email: str, reset_url: str) -> None:
        subject = self.subject_template_name
        html_message = render_to_string(
            self.email_template_name,
            {
                "email": email,
                "reset_url": reset_url,
            },
        )
        plain_message = strip_tags(html_message)

        send_mail_task.delay(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=self.from_email,
            recipient_list=[email],
            fail_silently=False,
        )
