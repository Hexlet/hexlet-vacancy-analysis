import logging
from typing import Sequence

from django.core.mail import send_mail

from app.celery import app
from app.services.auth.password_reset import configs

logger = logging.getLogger(__name__)


@app.task(
    bind=True,
    max_retries=configs.MAX_RETRIES,
    default_retry_delay=60,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
)
def send_mail_task(
    self,
    subject: str,
    message: str,
    html_message: str,
    from_email: str,
    recipient_list: Sequence[str],
    fail_silently: bool = False,
) -> None:
    """
    Асинхронная отправка email через Celery с автоматическими повторами.

    Использует настройки Django EMAIL_* и конфиг `configs.MAX_RETRIES`
    для повторных попыток.
    Поддерживает plain text и HTML версии письма.
    """
    current_retry = self.request.retries
    max_retries = self.max_retries
    try:
        send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=fail_silently,
        )
        logger.info(f"Password reset email sent to '{recipient_list}'")
    except Exception as e:
        logger.warning(
            f"Attempt {current_retry + 1} failed to send password "
            f"reset email to '{recipient_list}': {str(e)}"
        )
        if current_retry >= max_retries - 1:
            logger.error(
                f"Failed to send password reset email to '{recipient_list}' "
                f"after [{max_retries}] attempts"
            )
        if not fail_silently:
            raise
