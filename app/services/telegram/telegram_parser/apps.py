from django.apps import AppConfig


class TelegramParserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.services.telegram.telegram_parser"
