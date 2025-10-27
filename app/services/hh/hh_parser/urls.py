from django.urls import path

from . import views

urlpatterns = [
    path("", views.vacancy_list, name="vacancy_list"),
]
