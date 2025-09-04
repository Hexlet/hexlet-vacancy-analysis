from django.urls import path

from .views import TinkoffCallback, TinkoffLogin

urlpatterns = [
    path("", TinkoffLogin.as_view(), name="tinkoff_login"),
    path("collback/", TinkoffCallback.as_view(), name="tinkoff_callback"),
]
