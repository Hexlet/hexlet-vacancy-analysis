import logging

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views import View
from inertia import InertiaResponse  # type: ignore
from inertia import render as inertia_render

from .services.chat_service import ChatMessageService
from .services.exceptions import OpenAIError
from .services.openrouter import OpenRouterChat

logger = logging.getLogger(__name__)


class AIAssistantView(View):
    """
    Представление для AI-ассистента с поддержкой аутентифицированных
    и анонимных пользователей.
    Обрабатывает отображение страницы и обмен сообщениями с AI через OpenRouter API.
    """

    def _build_chat_service(self):
        ai_service = OpenRouterChat(
            api_key=settings.AI_API_KEY,
            model=settings.AI_API_MODEL,
            timeout=int(settings.AI_API_TIMEOUT),
        )
        return ChatMessageService(
            ai_service=ai_service,
            max_history_length=int(settings.CHAT_MAX_HISTORY_LENGTH),
        )

    def get(self, request: HttpRequest) -> InertiaResponse:
        """
        Отображает страницу ассистента.

        Возвращает страницу AIAssistantPage с историей сообщений пользователя.

        Args:
            request (HttpRequest): Объект запроса

        Returns:
            InertiaResponse: Страница с пропсами сообщений
        """
        chat_service = self._build_chat_service()
        messages = chat_service.get_history(
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key,
        )
        return inertia_render(
            request,
            "AIAssistantPage",
            props={
                "messages": messages,
            },
        )

    def post(self, request: HttpRequest) -> InertiaResponse:
        """
        Обрабатывает новое сообщение от пользователя.

        Отправляет сообщение в AI, сохраняет историю и возвращает ответ.
        Поддерживает аутентифицированных и анонимных пользователей.

        Args:
            request (HttpRequest): Запрос с сообщением

        Returns:
            JsonResponse: Ответ AI или ошибка с соответствующим статусом
        """
        message = request.POST.get("message")
        if message is None:
            return JsonResponse({"error": "Message is required"}, status=400)

        if not request.session.session_key:
            request.session.save()

        chat_service = self._build_chat_service()

        try:
            response = chat_service.hadle_message(
                user=request.user if request.user.is_authenticated else None,
                session_key=request.session.session_key,
                message=message,
            )
        except TimeoutError:
            logger.exception("AI request timeout")
            return JsonResponse({"error": "AI timeout"}, status=504)

        except OpenAIError:
            logger.exception("AI provider error")
            return JsonResponse({"error": "AI provider error"}, status=500)

        return JsonResponse({"message": response}, status=200)
