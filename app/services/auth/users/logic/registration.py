from django.contrib.auth import get_user_model
from django.db import OperationalError
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .. import exceptions as custom_ex
from .mail import safe_send_mail
from .tokens import account_activation_token
from .validators import (
    check_error_validation,
    normalize_email,
)

User = get_user_model()


def generate_activation_link(user, domain):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    activation_link = reverse("activate", kwargs={"uidb64": uid, "token": token})
    return f"http://{domain}{activation_link}"


def create_activation_mail(user, data):
    domain = data.get("domain")
    activate_url = generate_activation_link(user, domain)

    message = render_to_string(
        "activation_email.html",
        {
            "user": user,
            "activate_url": activate_url,
        },
    )
    return message


def create_user(data):
    email = normalize_email(data.get("email"))
    password = data.get("password")
    user = User.objects.create_user(email=email)
    user.set_password(password)
    user.is_active = False
    user.save()
    return user


def register_user(data):
    if check := check_error_validation(data):
        msg, status = check
        raise custom_ex.ValidationError(message=msg, code=status)

    try:
        user = create_user(data)
    except OperationalError:
        raise custom_ex.CreateUserError(message="Database Errors", code=500)

    try:
        message = create_activation_mail(user, data)
        safe_send_mail(message=message, recipient=[user.email])
    except custom_ex.SendEmailError:
        raise

    return user.id
