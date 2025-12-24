from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from inertia.test import InertiaTestCase  # type: ignore

from app.services.auth.password_reset import configs
from app.services.auth.password_reset.models import PasswordResetToken
from app.services.auth.password_reset.views import PasswordResetView

User = get_user_model()


class PasswordResetTestCase(InertiaTestCase):
    def setUp(self):
        super().setUp()
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
            "token_hash": hash("test_token"),
            "expires_at": expires_at,
        }
        self.token = PasswordResetToken.objects.create(**token_data)


@patch.object(PasswordResetView, "send_reset_email")
class PasswordResetTests(PasswordResetTestCase):
    def test_post_valid_email(self, mock_get_stats):
        mock_get_stats.return_value = None
        response = self.client.post(self.url, {"email": "testuser@example.com"})
        assert response.props["status_code"] == 200
        token = PasswordResetToken.objects.filter(user_id=self.user.id).first()
        assert token.token_hash
        assert token.expires_at > timezone.now()

    def test_post_invalid_email(self, mock_get_stats):
        mock_get_stats.return_value = None
        response = self.client.post(self.url, {"email": "invalid@example.com"})
        assert response.props["status_code"] == 200
        assert response.props["status"] == "ok"


class PasswordResetConfirmTests(PasswordResetTestCase):
    def test_get_valid_token(self):
        url = reverse("password_reset_confirm") + "?token=test_token"
        self.client.get(url)
        self.assertIncludesProps({"status_code": 200})

    def test_get_expired_token(self):
        PasswordResetToken.objects.create(
            user_id=self.user,
            token_hash=hash("expired_token"),
            expires_at=timezone.now() - timedelta(hours=1),
        )

        url = reverse_lazy("password_reset_confirm") + "?token=expired_token"
        self.client.get(url)
        self.assertIncludesProps({"status_code": 400})

    def test_post_valid_password(self):
        url = reverse_lazy("password_reset_confirm")
        data = {
            "token": self.token.token_hash,
            "newPassword": "StrongPass123!",
        }
        response = self.client.post(url, data)
        assert response.props["status_code"] == 200

        self.user.refresh_from_db()
        self.token.refresh_from_db()
        assert self.user.check_password("StrongPass123!")
        assert self.token.is_used

    def test_post_weak_password(self):
        url = reverse_lazy("password_reset_confirm")
        data = {"token": self.token.token_hash, "newPassword": "weak"}

        self.client.post(url, data)
        self.assertIncludesProps({"status_code": 422})

    def test_post_invalid_token(self):
        url = reverse_lazy("password_reset_confirm")
        data = {"token": "invalid_token", "newPassword": "StrongPass123!"}

        self.client.post(url, data)
        self.assertIncludesProps({"status_code": 400})
