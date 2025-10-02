from django.urls import path

from . import views

urlpatterns = [
    path('hh/', views.hh_vacancy_list, name='hh_vacancy_list'),
    path('superjob/', views.superjob_vacancy_list, name='superjob_vacancy_list'),
]
