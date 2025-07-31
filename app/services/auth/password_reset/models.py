from django.db import models

from app.services.auth.users.models import User


class PasswordResetToken(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    token_hash = models.CharField(255, null=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def mark_as_used(self):
        self.is_used = True
        self.save()

    @classmethod
    def mark_all_as_used(cls, user: User):
        queryset = cls.objects.filter(is_used=False, user_id=user)
        return queryset.update(is_used=True)
