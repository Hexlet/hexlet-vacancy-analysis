from django.utils.crypto import salted_hmac


def hash_token(token: str) -> str:
    return salted_hmac("password_reset", token).hexdigest()
