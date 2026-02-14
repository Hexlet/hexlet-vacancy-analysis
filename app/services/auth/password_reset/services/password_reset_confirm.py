from django.db import transaction

from ..models import PasswordResetToken
from .exceptions import InvalidToken


class ConfirmPasswordResetService:
    @transaction.atomic
    def confirm(self, *, token: str, new_password: str) -> None:
        reset_token = PasswordResetToken.find_active(token)

        if not reset_token:
            raise InvalidToken()

        user = reset_token.user

        user.set_password(new_password)
        user.save(update_fields=["password"])

        reset_token.mark_as_used()

    def is_valid(self, *, token: str) -> bool:
        return PasswordResetToken.find_active(token) is not None
