from django.urls import path

from .views import AIAssistantView

urlpatterns = [
    path("", AIAssistantView.as_view(), name="ai_assistant"),
]
