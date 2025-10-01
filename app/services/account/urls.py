from django.urls import path

from app.services.account.views import ProfileEditView

urlpatterns = [
    path("profile/", ProfileEditView.as_view(), name="account_profile_edit"),
]
