from celery import shared_task

from .sender import send_email_message, send_telegram_message


@shared_task
def send_email_message_task(to_email, subject, message):
    send_email_message(to_email, subject, message)


@shared_task
def send_telegram_message_task(chat_id, message):
    send_telegram_message(chat_id, message)