from django.db import models


class ChatMessage(models.Model):
    message_id = models.IntegerField(null=True, default=0, verbose_name=("message_id"))
    user_id = models.IntegerField(null=True, default=0, verbose_name=("user_id"))
    chat_id = models.IntegerField(null=True, default=0, verbose_name=("chat_id"))
    last_message_id = models.IntegerField(
        verbose_name=("last_message_id"), blank=True, null=True
    )
    username = models.CharField(
        max_length=255, unique=True, verbose_name=("user_name")
    )
    first_name = models.CharField(
        max_length=255, unique=True, verbose_name=("first_name"), null=True, blank=True
    )
    last_name = models.CharField(
        max_length=255, unique=True, verbose_name=("last_name"), null=True, blank=True
    )
    status = models.CharField(
        max_length=10, verbose_name=(
            "channel_status"), default="active", null=True, blank=True
    )
    text = models.CharField(
        max_length=255, unique=True, verbose_name=("text"), null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="message_date")

    def __str__(self):
        return f"{self.username or 'User'}: {self.text[:30]}"

    class InertiaMeta:
        fields = (
            'message_id',
            'user_id',
            'chat_id',
            'last_message_id',
            'username',
            'first_name',
            'last_name',
            'status',
            'text',
            'created_at'
        )

