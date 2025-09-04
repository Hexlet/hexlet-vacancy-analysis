from django.urls import path

from app.services.auth.vk_id import views

urlpatterns = [
    path("", views.vk_draft_login, name="vk_login"),
    path("start/", views.vk_start_auth, name="vk_start"),
    path("callback/", views.vk_auth_callback, name="vk_callback"),
]