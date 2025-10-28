import re

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .phone import normalize_phone_number

User = get_user_model()


REQUIRED_FIELDS_MSG = "All fields are required"
INVALID_EMAIL_MSG = "Invalid email"
SHORT_PASSWORD_MSG = "Pass must contain at least 8 characters, \
                        mininum one digital and one big letter"
PASS_NO_MATCH_MSG = "The passwords entered do not match."
EMAIL_ALREADY_EXIST_MSG = "This Email already exists."
ACCEPT_TERMS_MSG = "Terms must be accepted"
INVALID_PHONE_MSG = "Invalid phone"
PHONE_ALREADY_EXIST_MSG = "Phone already in use"


def normalize_email(email):
    email = email.strip().lower()
    if email.endswith("@gmail.com"):
        local, domain = email.split("@")
        local = local.split("+")[0]
        local = local.replace(".", "")
        return f"{local}@{domain}"
    return email


def check_error_validation(register_data):
    email = register_data.get("email")
    password = register_data.get("password")
    password_again = register_data.get("passwordAgain")
    accept_terms = register_data.get("acceptTerms")
    phone = register_data.get("phone")

    if not all([email, password, password_again, accept_terms, phone]):
        return REQUIRED_FIELDS_MSG, 400
    if validate_email(email):
        return INVALID_EMAIL_MSG, 400
    if password != password_again:
        return PASS_NO_MATCH_MSG, 400
    if not re.match(r"^(?=.*[A-Z])(?=.*\d).{8,}$", password):
        return SHORT_PASSWORD_MSG, 400
    if not accept_terms:
        return ACCEPT_TERMS_MSG, 400
    # формат телефона и проверка уникальности
    try:
        normalized_phone = normalize_phone_number(phone)
    except ValidationError:
        return INVALID_PHONE_MSG, 400
    if User.objects.filter(phone=normalized_phone.number).exists():
        return PHONE_ALREADY_EXIST_MSG, 409
    email = normalize_email(email)
    if User.objects.filter(email=email, is_active=True).exists():
        return EMAIL_ALREADY_EXIST_MSG, 409

    return None
