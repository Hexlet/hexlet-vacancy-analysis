import logging

from celery import shared_task
from django.core.mail import send_mail

from app.services.auth.password_reset import configs

logger = logging.getLogger(__name__)


@shared_task(
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
    recipient_list: list = None,
    fail_silently: bool = False,
):
    """
    Асинхронная задача для отправки электронного письма с автоматической повторной
    попыткой.

    Использует Celery для фоновой обработки и настроенную логику перезапуска при ошибках.
    Поддерживает HTML-форматирование сообщений и позволяет указывать адрес отправителя.

    Parameters:
    ----------
    self : Task
        Ссылка на текущую задачу Celery (автоматически передается).
    subject : str
        Тема письма.
    message : str
        Текст письма в plain text формате.
    html_message : str
        Текст письма в HTML-формате (опционально).
    from_email : str
        Адрес отправителя.
    recipient_list : list, optional
        Список адресов получателей. По умолчанию None.
    fail_silently : bool, optional
        Если True, ошибки будут логироваться, но не прерывать выполнение.
        По умолчанию False.

    Returns:
    -------
    None

    Raises:
    ------
    Exception
        Если `fail_silently=False` и отправка письма не удалась после всех попыток.

    Notes:
    -----
    - Задача поддерживает автоматическую повторную отправку (`autoretry`) при
    возникновении исключений.
    - Максимальное количество попыток определяется значением `configs.MAX_RETRIES`.
    - При каждой неудачной попытке записывается лог с уровнем WARNING.
    - Логирование успешной отправки выполняется на уровне INFO.
    - Для работы требуется корректная настройка email-бэкенда Django (EMAIL_* параметры).

    Examples:
    -------
    >>> send_mail_task.delay(
    ...     subject="Сброс пароля",
    ...     message="Инструкции по сбросу пароля...",
    ...     html_message="<p>Инструкции по <strong>сбросу пароля</strong></p>",
    ...     recipient_list=["user@example.com"],
    ... )
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
