from django.urls import path

from app.services.auth.yandex_id import views

urlpatterns = [
    path("start/", views.start_auth, name="yandex_auth"),
    path("callback/", views.auth_callback, name="yandex_callback"),
]
