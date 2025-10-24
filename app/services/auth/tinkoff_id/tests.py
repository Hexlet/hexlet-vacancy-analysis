from unittest.mock import MagicMock, patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase
from django.urls import reverse

from .views import TinkoffCallback, TinkoffLogin

User = get_user_model()


class TinkoffLoginTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse("tinkoff_login")

    def test_get_redirects_to_tinkoff_auth(self):
        request = self.factory.get(self.url)

        # Добавляем сессию к запросу
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session.save()

        response = TinkoffLogin.as_view()(request)

        # Проверяем редирект
        self.assertEqual(response.status_code, 302)
        self.assertTrue(settings.TINKOFF_ID_AUTH_URL in response.url)

        # Проверяем параметры в URL
        self.assertIn(
            "client_id=" + settings.TINKOFF_ID_CLIENT_ID, response.url
        )
        self.assertIn(
            "redirect_uri=" + settings.TINKOFF_ID_REDIRECT_URI, response.url
        )
        self.assertIn("response_type=code", response.url)

        # Проверяем, что state сохранен в сессии
        self.assertIn("state", request.session)


class TinkoffCallbackTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse("tinkoff_callback")
        self.state = "test_state_123"
        self.code = "test_code_123"
        self.email = "test@example.com"

        # Мокируем ответы API
        self.token_response = {
            "access_token": "test_access_token",
            "token_type": "Bearer",
            "expires_in": 3600,
        }

        self.introspect_response = {
            "active": True,
            "scope": settings.TINKOFF_ID_SCOPE,
        }

        self.user_info_response = {
            "email": self.email,
            "sub": "1234567890",
        }

    def _add_session(self, request):
        """Добавляем сессию к запросу"""
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(request)
        request.session["state"] = self.state
        request.session.save()
        return request

    @patch("app.services.auth.tinkoff_id.views.requests.post")
    def test_successful_authentication(self, mock_post):
        # Настраиваем моки для последовательных вызовов requests.post
        mock_post.side_effect = [
            MagicMock(status_code=200, json=lambda: self.token_response),
            MagicMock(status_code=200, json=lambda: self.introspect_response),
            MagicMock(status_code=200, json=lambda: self.user_info_response),
        ]

        request = self.factory.get(
            self.url,
            {
                "state": self.state,
                "code": self.code,
            },
        )
        request = self._add_session(request)
        response = TinkoffCallback.as_view()(request)

        # Проверяем успешный редирект
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

        # Проверяем, что пользователь создан и залогинен
        user = User.objects.get(email=self.email)
        self.assertTrue(user.is_authenticated)

        # Проверяем, что state удален из сессии
        self.assertNotIn("state", request.session)

    @patch("app.services.auth.tinkoff_id.views.requests.post")
    def test_invalid_state(self, mock_post):
        request = self.factory.get(
            self.url,
            {
                "state": "invalid_state",
                "code": self.code,
            },
        )
        request = self._add_session(request)

        response = TinkoffCallback.as_view()(request)

        self.assertEqual(response.props["status_code"], 403)
        self.assertIn("Invalid state parameter", str(response.content))

    @patch("app.services.auth.tinkoff_id.views.requests.post")
    def test_missing_code(self, mock_post):
        request = self.factory.get(
            self.url,
            {
                "state": self.state,
            },
        )
        request = self._add_session(request)

        response = TinkoffCallback.as_view()(request)

        self.assertEqual(response.props["status_code"], 403)
        self.assertIn("Missing code parameter", str(response.content))

    @patch("app.services.auth.tinkoff_id.views.requests.post")
    def test_token_request_failure(self, mock_post):
        mock_post.return_value = MagicMock(status_code=400)

        request = self.factory.get(
            self.url,
            {
                "state": self.state,
                "code": self.code,
            },
        )
        request = self._add_session(request)

        response = TinkoffCallback.as_view()(request)

        self.assertEqual(response.props["status_code"], 403)
        self.assertIn("Failed to get access token", str(response.content))

    @patch("app.services.auth.tinkoff_id.views.requests.post")
    def test_introspect_request_failure(self, mock_post):
        mock_post.side_effect = [
            MagicMock(status_code=200, json=lambda: self.token_response),
            MagicMock(status_code=400),
        ]

        request = self.factory.get(
            self.url,
            {
                "state": self.state,
                "code": self.code,
            },
        )
        request = self._add_session(request)

        response = TinkoffCallback.as_view()(request)

        self.assertEqual(response.props["status_code"], 403)
        self.assertIn("Failed to get introspect token", str(response.content))

    @patch("app.services.auth.tinkoff_id.views.requests.post")
    def test_missing_scope(self, mock_post):
        # Меняем ответ introspection, убирая нужные scope
        invalid_introspect = self.introspect_response.copy()
        invalid_introspect["scope"] = []

        mock_post.side_effect = [
            MagicMock(status_code=200, json=lambda: self.token_response),
            MagicMock(status_code=200, json=lambda: invalid_introspect),
        ]

        request = self.factory.get(
            self.url,
            {
                "state": self.state,
                "code": self.code,
            },
        )
        request = self._add_session(request)

        response = TinkoffCallback.as_view()(request)

        self.assertEqual(response.props["status_code"], 403)
        self.assertIn("Missing scope", str(response.content))

    @patch("app.services.auth.tinkoff_id.views.requests.post")
    def test_missing_email(self, mock_post):
        # Меняем user_info, убирая email
        invalid_user_info = self.user_info_response.copy()
        invalid_user_info.pop("email")

        mock_post.side_effect = [
            MagicMock(status_code=200, json=lambda: self.token_response),
            MagicMock(status_code=200, json=lambda: self.introspect_response),
            MagicMock(status_code=200, json=lambda: invalid_user_info),
        ]

        request = self.factory.get(
            self.url,
            {
                "state": self.state,
                "code": self.code,
            },
        )
        request = self._add_session(request)

        response = TinkoffCallback.as_view()(request)

        self.assertEqual(response.props["status_code"], 403)
        self.assertIn("User has no email", str(response.content))
