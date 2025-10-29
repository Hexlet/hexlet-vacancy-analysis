from django.urls import path

from . import views

urlpatterns = [
    path("", views.superjob_list, name="superjob_list"),
]
