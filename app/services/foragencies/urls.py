from django.urls import path

from . import views

urlpatterns = [
    path("", views.AgencyView.as_view(), name="foragencies_page"),
]
