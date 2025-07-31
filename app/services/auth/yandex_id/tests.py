from types import SimpleNamespace
from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import resolve, reverse

from app.services.auth.yandex_id import views


class YandexIDURLTests(TestCase):
    """
    проверяем, что маршруты и имена URL-ов остались прежними.
    """

    def test_urls_resolve(self):
        self.assertEqual(resolve("/auth/yandex/").func, views.draft_login)
        self.assertEqual(resolve("/auth/yandex/start/").func, views.start_auth)
        self.assertEqual(resolve("/auth/yandex/callback/").func, views.auth_callback)

    def test_reverse_names(self):
        self.assertEqual(reverse("yandex_login"), "/auth/yandex/")
        self.assertEqual(reverse("yandex_auth"), "/auth/yandex/start/")
        self.assertEqual(reverse("yandex_callback"), "/auth/yandex/callback/")


class YandexIDViewsTests(TestCase):
    """
    проверки draft-страницы, старта OAuth и callback-а.
    """

    def setUp(self):
        self.client = Client()

    # ----- draft_login ------------------------------------------------------

    def test_draft_login_shows_link(self):
        resp = self.client.get(reverse("yandex_login"))
        self.assertContains(resp, "Войти через Yandex ID")

    # ----- start_auth -------------------------------------------------------

    def test_start_auth_redirects(self):
        resp = self.client.get(reverse("yandex_auth"))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(
            resp["Location"].startswith("https://oauth.yandex.ru/authorize"),
            resp["Location"],
        )

    # ----- auth_callback: невалидный state ----------------------------------

    def test_auth_callback_invalid_state(self):
        url = reverse("yandex_callback") + "?state=wrong&code=any"
        resp = self.client.get(url)
        self.assertContains(resp, "Invalid OAuth state", status_code=400)

    # ----- auth_callback: backend вернул None -------------------------------

    def test_auth_callback_authentication_failed(self):
        """
        если YandexBackend ничего не вернул, получаем 400.
        """
        # сначала запрашиваем старт, чтобы появился правильный state
        _ = self.client.get(reverse("yandex_auth"))
        state = self.client.session["oauth_state"]

        with patch(
            "app.services.auth.yandex_id.views.authenticate", return_value=None
        ):
            resp = self.client.get(
                reverse("yandex_callback") + f"?state={state}&code=badcode"
            )
        self.assertContains(resp, "Authentication failed", status_code=400)

    # ----- auth_callback: успешный OAuth-flow -------------------------------

    @patch("app.services.auth.yandex_id.backend.requests.get")
    @patch("app.services.auth.yandex_id.backend.requests.post")
    def test_full_oauth_flow(self, mock_post, mock_get):
        """
        проверяем happy-path: обмен code -> token, получение профиля,
        сохранение пользователя, логин и редирект.
        """

        # мокаем запрос code  ->  token
        mock_post.return_value = SimpleNamespace(
            raise_for_status=lambda: None,
            json=lambda: {"access_token": "token123"},
        )

        # мокаем запрос профиля
        mock_get.return_value = SimpleNamespace(
            raise_for_status=lambda: None,
            json=lambda: {
                "default_email": "test@yandex.com",
                "first_name": "Ivan",
                "last_name": "Ivanov",
            },
        )

        # генерируем state (start_auth) — чтобы прошла проверка
        resp_start = self.client.get(reverse("yandex_auth"))
        self.assertEqual(resp_start.status_code, 302)
        state = self.client.session["oauth_state"]

        # вызываем callback с правильным state & любым code
        resp_cb = self.client.get(
            reverse("yandex_callback") + f"?state={state}&code=abc"
        )
        self.assertRedirects(resp_cb, reverse("yandex_login"))

        # убеждаемся, что пользователь создан и данные записаны
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.get(email="test@yandex.com")
        self.assertEqual((user.first_name, user.last_name), ("Ivan", "Ivanov"))
