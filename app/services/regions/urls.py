from django.urls import path

from . import views

urlpatterns = [
    path('<str:region_id>', views.RegionView.as_view(), name='region_page'),
]