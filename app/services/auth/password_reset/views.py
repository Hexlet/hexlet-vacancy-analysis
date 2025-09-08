from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.html import strip_tags
from django.views import View
from django_ratelimit.decorators import ratelimit
from inertia import location, render

from . import configs
from .logs.logger import get_logger
from .models import PasswordResetToken
from .validators import is_valid_password

User = get_user_model()
logger = get_logger(__name__)


class PasswordResetView(View):
    subject_template_name = "шаблон_тема_письма.txt"
    email_template_name = "шаблон_тело_письма.html"
    from_email = "test@test.com"
    token_generator = PasswordResetTokenGenerator

    def get(self, request):
        logger.info("Password reset service started")
        return render(
            request,
            "PasswordResetPage",
            props={"status": "ok", "status_code": 200},
        )

    @method_decorator(ratelimit(key="ip", rate="3/h"))
    @method_decorator(ratelimit(key="post:email", rate="3/h"))
    def post(self, request):
        was_limited = getattr(request, "limited", False)
        logger.info(f"Limit reached: [{was_limited}]")
        if was_limited:
            return render(
                request,
                "ErrorPage",
                props={
                    "message": "Too many requests. Try again later.",
                    "status_code": 429,
                },
            )

        email = request.POST.get("email")
        if not email:
            return render(
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
            logger.error(f"['{email}']: email does not belong to any user")
            user = None
        if user:
            PasswordResetToken.mark_all_as_used(user)
            token_hash = self.token_generator().make_token(user)
            current_time = timezone.now()
            time_out = timedelta(configs.PASSWORD_RESET_TIMEOUT)
            expires_at = current_time + time_out
            reset_url = request.build_absolute_uri(
                reverse("link_in_mail") + f"?token={token_hash}"
            )
            self.send_reset_email(email, reset_url)
            PasswordResetToken.objects.create(
                user_id=user,
                token_hash=token_hash,
                expires_at=expires_at,
            )
        return render(
            request,
            "PasswordResetCompletePage",
            props={"status": "ok", "status_code": 200},
        )

    def send_reset_email(self, email, reset_url):
        # subject = render_to_string(self.subject_template_name)
        # html_message = render_to_string(
        #     self.email_template_name,
        #     {
        #         "reset_url": reset_url,
        #     },
        # )
        subject = self.subject_template_name
        html_message = self.email_template_name

        plain_message = strip_tags(html_message)
        max_retries = configs.MAX_RETRIES
        for attempt in range(max_retries):
            try:
                send_mail(
                    subject=subject,
                    message=plain_message,
                    html_message=html_message,
                    from_email=self.from_email,
                    recipient_list=[email],
                    fail_silently=False,
                )
                logger.info(f"Password reset email sent to ['{email}']")
                break
            except Exception as e:
                logger.warning(
                    f"Attempt {attempt + 1} failed to send password "
                    f"reset email to ['{email}']: {str(e)}"
                )
                if attempt == max_retries - 1:
                    logger.error(
                        f"Failed to send password reset email to ['{email}'] "
                        f"after [{max_retries}] attempts"
                    )


def redirect_mail_link(request):
    token = request.GET.get("token")
    url = reverse("password_reset_confirm") + f"?token={token}"
    return location(url)


class PasswordResetConfirmView(View):
    def get(self, request):
        token = request.GET.get("token")
        reset_token = PasswordResetToken.objects.filter(
            token_hash=token, is_used=False
        ).first()
        if reset_token:
            if reset_token.expires_at > timezone.now():
                return render(
                    request,
                    "PasswordResetConfirmPage",
                    props={
                        "status": "ok",
                        "status_code": 200,
                        "data": {"token": token},
                    },
                )
        logger.error(f"['{token}']: token is expired or invalid")
        return render(
            request,
            "ErrorPage",
            props={
                "status": "Bad Request",
                "status_code": 400,
                "message": "Ссылка недействительна или истекла",
            },
        )

    def post(self, request):
        token = request.POST.get("token")
        new_password = request.POST.get("newPassword")
        if not is_valid_password(new_password):
            return render(
                request,
                "PasswordResetConfirmPage",
                props={
                    "status": "Unprocessable Entity",
                    "status_code": 422,
                    "message": "Слабый пароль",
                    "data": {"token": token},
                },
            )
        reset_token = PasswordResetToken.objects.filter(
            token_hash=token, is_used=False
        ).first()
        if reset_token:
            if reset_token.expires_at > timezone.now():
                user = User.objects.get(id=reset_token.user_id.pk)
                user.set_password(new_password)
                user.save()
                reset_token.mark_as_used()
                return render(
                    request,
                    "HomePage",
                    props={"status": "ok", "status_code": 200},
                )
        return render(
            request,
            "ErrorPage",
            props={
                "status": "Bad Request",
                "status_code": 400,
                "message": "Недействительный токен",
            },
        )
