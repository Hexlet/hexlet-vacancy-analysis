from django import forms
from django.contrib.auth.password_validation import validate_password


class PasswordResetForm(forms.Form):
    email = forms.EmailField()


class PasswordResetConfirmForm(forms.Form):
    token = forms.CharField()
    new_password = forms.CharField()

    def clean_new_password(self):
        password = self.cleaned_data["new_password"]
        validate_password(password)
        return password
