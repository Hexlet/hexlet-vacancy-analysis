from datetime import timedelta
from django.urls import reverse_lazy
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.core import mail
from requests import patch
from app.services.auth.password_reset import configs
from app.services.auth.password_reset.models import PasswordResetToken
from django.utils import timezone
from app.services.auth.password_reset.logs.logger import *

User = get_user_model()
logger = logging.getLogger(__name__)


class PasswordResetTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse_lazy("password_reset")
        user_data = {
            "email": "testuser@example.com",
            "password": "password123",
        }
        self.user = User.objects.create_user(**user_data)
        current_time = timezone.now()
        time_out = timedelta(configs.PASSWORD_RESET_TIMEOUT)
        expires_at = current_time + time_out
        token_data = {
            "user_id": self.user,
            "token_hash": "test_token",
            "expires_at": expires_at,
        }
        self.token = PasswordResetToken.objects.create(**token_data)


class PasswordResetTests(PasswordResetTestCase):
    def test_post_valid_email(self):
        response = self.client.post(
            self.url, {"email": "testuser@example.com"}
        )

        assert response.status_code == 200
        token = PasswordResetToken.objects.filter(user_id=self.user.id).first()
        assert token.token_hash
        assert token.expires_at > timezone.now()
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == ["testuser@example.com"]

    def test_post_invalid_email(self):
        response = self.client.post(self.url, {"email": "invalid@example.com"})
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class PasswordResetConfirmTests(PasswordResetTestCase):
    def test_get_valid_token(self):
        url = (
            reverse_lazy("password_reset_confirm")
            + f"?token={self.token.token_hash}"
        )
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_get_expired_token(self):
        expired_token = PasswordResetToken.objects.create(
            user_id=self.user,
            token_hash="expired_token",
            expires_at=timezone.now() - timedelta(hours=1),
        )

        url = (
            reverse_lazy("password_reset_confirm")
            + f"?token={expired_token.token_hash}"
        )
        response = self.client.get(url)
        assert response.status_code == 400
        assert "Ссылка недействительна" in response.json()["message"]

    def test_post_valid_password(self):
        url = reverse_lazy("password_reset_confirm")
        data = {
            "token": self.token.token_hash,
            "newPassword": "StrongPass123!",
        }
        response = self.client.post(url, data)
        assert response.status_code == 200

        self.user.refresh_from_db()
        self.token.refresh_from_db()
        assert self.user.check_password("StrongPass123!")
        assert self.token.is_used

    def test_post_weak_password(self):
        url = reverse_lazy("password_reset_confirm")
        data = {"token": self.token.token_hash, "newPassword": "weak"}

        response = self.client.post(url, data)
        assert response.status_code == 422
        assert "Слабый пароль" in response.json()["message"]

    def test_post_invalid_token(self):
        url = reverse_lazy("password_reset_confirm")
        data = {"token": "invalid_token", "newPassword": "StrongPass123!"}

        response = self.client.post(url, data)
        assert response.status_code == 400
        assert "Недействительный токен" in response.json()["message"]
