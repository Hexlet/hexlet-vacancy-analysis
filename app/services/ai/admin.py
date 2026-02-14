from django.contrib import admin

from .models import ChatMessage


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("user_display", "message_summary", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at", "user")

    def user_display(self, obj):
        if obj.user:
            return obj.user.username
        else:
            return str(obj.session_key)[0:10] + "..."

    user_display.short_description = "Пользователь"  # type: ignore

    def message_summary(self, obj):
        return str(obj.messages)[0:200] + "..."

    message_summary.short_description = "Сообщения"  # type: ignore
