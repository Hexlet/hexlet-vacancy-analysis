from django.urls import path

from . import views

urlpatterns = [
    path("", views.AIAssistantView.as_view(), name="ai_assistant"),
]
