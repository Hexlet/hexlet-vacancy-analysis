from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>', views.ShowRegionView.as_view(), name='show_region'),
]