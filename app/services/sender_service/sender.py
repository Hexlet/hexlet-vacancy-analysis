import asyncio

from django.conf import settings
from django.core.mail import send_mail
from telegram import Bot

from app.settings import TELEGRAM_BOT_TOKEN


def send_email_message(to_email, subject, message):
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [to_email],
        fail_silently=False,
    )


def send_telegram_message(chat_id, message):
    token = TELEGRAM_BOT_TOKEN
    bot = Bot(token=token)
    asyncio.run(bot.send_message(chat_id=chat_id, text=message))
