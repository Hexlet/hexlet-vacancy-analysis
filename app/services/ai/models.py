from django.db import models
from django.utils import timezone

from ..auth.users.models import User


class ChatMessage(models.Model):
    """
    Модель для хранения сообщений в диалоге
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Пользователь",
    )
    messages = models.JSONField(blank=True, verbose_name="Сообщения")
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Ключ сессии",
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        ordering = ("created_at",)
        verbose_name = "Сообщение чата"
        verbose_name_plural = "Сообщения чата"

        constraints = [
            models.UniqueConstraint(
                fields=["user"],
                condition=models.Q(user__isnull=False),
                name="unique_user_messages",
            ),
            models.UniqueConstraint(
                fields=["session_key"],
                condition=models.Q(session_key__isnull=False, user__isnull=True),
                name="unique_session_messages",
            ),
        ]
