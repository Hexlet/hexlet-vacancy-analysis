from django.urls import path

from app.services.auth.github import views

urlpatterns = [
    path("", views.draft_login, name="github_login"),
    path("start/", views.start_auth, name="github_auth"),
    path("callback/", views.auth_callback, name="github_callback"),
]