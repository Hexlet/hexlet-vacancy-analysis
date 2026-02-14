from django.db import models
from django.utils import timezone

from app.services.auth.users.models import User

from .utils import hash_token


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token_hash = models.CharField(null=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def mark_as_used(self):
        self.is_used = True
        self.save()

    @classmethod
    def mark_all_as_used(cls, user: User):
        queryset = cls.objects.filter(is_used=False, user=user)
        return queryset.update(is_used=True)

    @classmethod
    def find_active(cls, raw_token: str):
        return (
            cls.objects.filter(
                token_hash=hash_token(raw_token),
                is_used=False,
                expires_at__gt=timezone.now(),
            )
            .select_related("user")
            .first()
        )
