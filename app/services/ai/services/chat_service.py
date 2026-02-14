import logging

from app.services.auth.users.models import User

from ..models import ChatMessage
from .openrouter import OpenRouterChat

logger = logging.getLogger(__name__)


class ChatMessageService:
    """Сервис для работы с сообщениями чата"""

    def __init__(
        self,
        ai_service: OpenRouterChat,
        max_history_length: int = 10,
    ) -> None:
        self.ai_service = ai_service
        self.max_history_length = max_history_length

    def hadle_message(self, *, user: User, session_key: str, message: str) -> str:
        history = self.get_history(user=user, session_key=session_key)
        response = self.ai_service.get_response(message, history)
        new_history = self._append_and_trim(history, message, response)
        self._save_history(user=user, session_key=session_key, history=new_history)
        return response

    def get_history(self, *, user: User | None, session_key: str | None) -> list[dict]:
        chat = self._get_chat(user=user, session_key=session_key)
        return chat.messages if chat else []

    def _append_and_trim(
        self, history: list[dict], user_msg: str, assistant_msg: str
    ) -> list[dict]:
        history = history + [
            {"role": "user", "content": user_msg},
            {"role": "assistant", "content": assistant_msg},
        ]

        if len(history) > self.max_history_length * 2:
            history = history[-self.max_history_length * 2 :]

        return history

    def _save_history(self, *, user: User, session_key: str, history: list[dict]):
        ChatMessage.objects.update_or_create(
            user=user,
            session_key=session_key if not user else None,
            defaults={"messages": history},
        )

    def _get_chat(
        self, *, user: User | None, session_key: str | None
    ) -> ChatMessage | None:
        if user:
            return ChatMessage.objects.filter(user=user).first()
        return ChatMessage.objects.filter(
            session_key=session_key, user__isnull=True
        ).first()
