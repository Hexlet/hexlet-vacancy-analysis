from django.apps import AppConfig


class PasswordResetConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "app.services.auth.password_reset"
