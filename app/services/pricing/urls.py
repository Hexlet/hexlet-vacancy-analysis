from django.urls import path

from . import views

urlpatterns = [
    path('', views.PricingView.as_view(), name='pricing_page'),
]