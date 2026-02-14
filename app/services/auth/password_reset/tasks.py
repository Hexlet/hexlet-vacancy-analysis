import logging
import smtplib

from django.conf import settings
from django.core.mail import send_mail

from app.celery import app

logger = logging.getLogger(__name__)


TRANSIENT_EMAIL_ERRORS = (
    smtplib.SMTPServerDisconnected,
    smtplib.SMTPConnectError,
    smtplib.SMTPHeloError,
    TimeoutError,
)


@app.task(bind=True, max_retries=int(settings.MAX_RETRIES_TO_SEND))
def send_mail_task(
    self,
    subject: str,
    message: str,
    html_message: str,
    from_email: str,
    recipient_list: list[str],
    fail_silently: bool = False,
) -> None:
    """
    Асинхронная отправка email через Celery с автоматическими повторами.

    Использует настройки Django EMAIL_* и конфиг `configs.MAX_RETRIES`
    для повторных попыток.
    Поддерживает plain text и HTML версии письма.
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=fail_silently,
        )
        logger.info("Email sent to %s", recipient_list)
    except TRANSIENT_EMAIL_ERRORS as e:
        logger.warning("Transient email error: %e", e)
        raise self.retry(exc=e, countdown=60)
    except smtplib.SMTPRecipientsRefused:
        logger.error("Invalid resipient: %s", recipient_list)
        raise
