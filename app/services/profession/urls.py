from django.urls import path

from .views import ProfessionView

urlpatterns = [
    path("<slug:profession_slug>/", ProfessionView.as_view(), name='profession_page')
]