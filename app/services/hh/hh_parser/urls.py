from django.urls import path

from . import views

urlpatterns = [
    path("", views.hh_vacancy_parse, name="hh_vacancy_parse"),
]
