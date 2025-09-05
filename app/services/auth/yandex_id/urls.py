from django.urls import path

from app.services.auth.yandex_id import views

urlpatterns = [
    path("", views.draft_login, name="yandex_login"),
    path("start/", views.start_auth, name="yandex_auth"),
    path("callback/", views.auth_callback, name="yandex_callback"),
    path("email/register/", views.email_register, name="yandex_email_register"),
    path("email/login/", views.email_login, name="yandex_email_login"),
]
