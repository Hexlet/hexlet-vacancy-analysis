from django.urls import path

from . import views

urlpatterns = [
    path("", views.superjob_vacancy_parse, name="superjob_vacancy_parse"),
]
