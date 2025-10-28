from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import resolve, reverse

from app.services.auth.users.models import UserIdentity
from app.services.auth.yandex_id import views

User = get_user_model()


class YandexIDURLTests(TestCase):
    """
    проверяем, что маршруты и имена URL-ов остались прежними.
    """

    def test_urls_resolve(self):
        self.assertEqual(resolve("/auth/yandex/start/").func, views.start_auth)
        self.assertEqual(resolve("/auth/yandex/callback/").func, views.auth_callback)

    def test_reverse_names(self):
        self.assertEqual(reverse("yandex_auth"), "/auth/yandex/start/")
        self.assertEqual(reverse("yandex_callback"), "/auth/yandex/callback/")


class YandexIDViewsTests(TestCase):
    """
    проверки draft-страницы, старта OAuth и callback-а и логики next.
    """

    def setUp(self):
        self.client = Client()

    # (draft login removed)

    # ----- start_auth (обычный визит, 302) ---------------------------------

    def test_start_auth_redirects_and_sets_state(self):
        resp = self.client.get(reverse("yandex_auth"))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(
            resp["Location"].startswith("https://oauth.yandex.ru/authorize"),
            resp["Location"],
        )
        # state должен появиться в сессии
        self.assertIn("oauth_state", self.client.session)
        # и карта flows с привязкой next к state
        state = self.client.session["oauth_state"]
        flows = self.client.session.get("oauth_flows", {})
        self.assertIn(state, flows)
        self.assertIn("next", flows[state])
        self.assertIsNone(flows[state]["next"])

    def test_start_auth_stores_valid_next_from_query(self):
        resp = self.client.get(reverse("yandex_auth") + "?next=/some/path")
        self.assertEqual(resp.status_code, 302)
        state = self.client.session["oauth_state"]
        flows = self.client.session.get("oauth_flows", {})
        self.assertEqual(flows[state]["next"], "/some/path")

    def test_start_auth_ignores_external_next(self):
        resp = self.client.get(reverse("yandex_auth") + "?next=https://evil.com/hack")
        self.assertEqual(resp.status_code, 302)
        state = self.client.session["oauth_state"]
        flows = self.client.session.get("oauth_flows", {})
        # внешний next должен быть отфильтрован
        self.assertIsNone(flows[state]["next"])

    def test_start_auth_uses_referer_when_no_next(self):
        resp = self.client.get(reverse("yandex_auth"), **{"HTTP_REFERER": "/from/page"})
        self.assertEqual(resp.status_code, 302)
        state = self.client.session["oauth_state"]
        flows = self.client.session.get("oauth_flows", {})
        self.assertEqual(flows[state]["next"], "/from/page")

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

        with patch("app.services.auth.yandex_id.views.authenticate", return_value=None):
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
        self.assertRedirects(resp_cb, reverse("auth_draft"))

        # убеждаемся, что пользователь создан и данные записаны
        user = User.objects.get(email="test@yandex.com")
        self.assertEqual((user.first_name, user.last_name), ("Ivan", "Ivanov"))

    # ----- auth_callback: возврат на next -----------------------------------

    def test_auth_callback_redirects_to_next_and_cleans_flow(self):
        """
        стартуем с валидным next, затем колбэк редиректит туда же,
        а запись в flows удаляется.
        """
        # старт с next
        resp_start = self.client.get(reverse("yandex_auth") + "?next=/welcome")
        self.assertEqual(resp_start.status_code, 302)
        state = self.client.session["oauth_state"]
        self.assertEqual(self.client.session["oauth_flows"][state]["next"], "/welcome")

        # готовим пользователя и удачную authenticate
        user = User.objects.create_user(email="u@example.com", password="Password2025")
        user.backend = "django.contrib.auth.backends.ModelBackend"  # важно для login()
        with patch("app.services.auth.yandex_id.views.authenticate", return_value=user):
            resp_cb = self.client.get(
                reverse("yandex_callback") + f"?state={state}&code=ok"
            )

        # конечной страницы/welcome может не быть -> не ходим за ней
        self.assertRedirects(resp_cb, "/welcome", fetch_redirect_response=False)

        # запись по state должна быть удалена (одноразовость)
        flows = self.client.session.get("oauth_flows", {})
        self.assertNotIn(state, flows)

    def test_auth_callback_with_bad_next_falls_back(self):
        """
        стартуем с внешним next -> он игнорируется, после колбэка редирект на дефолт.
        """
        _ = self.client.get(reverse("yandex_auth") + "?next=https://evil.com/path")
        state = self.client.session["oauth_state"]

        user = User.objects.create_user(email="x@example.com", password="Password2025")
        user.backend = "django.contrib.auth.backends.ModelBackend"
        with patch("app.services.auth.yandex_id.views.authenticate", return_value=user):
            resp_cb = self.client.get(
                reverse("yandex_callback") + f"?state={state}&code=ok"
            )
        self.assertRedirects(resp_cb, reverse("auth_draft"))


class YandexIDLinkFlowTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_start_auth_sets_link_flag(self):
        resp = self.client.get(reverse("yandex_auth") + "?link=1")
        self.assertEqual(resp.status_code, 302)
        state = self.client.session["oauth_state"]
        flows = self.client.session.get("oauth_flows", {})
        self.assertTrue(flows[state]["link"])  # link flag saved

    def test_apply_blocked_when_not_linked(self):
        self.client.force_login(
            User.objects.create_user(email="me@example.com", password="Password2025")
        )
        resp = self.client.get(reverse("yandex_auth") + "?apply=1")
        self.assertRedirects(
            resp, reverse("auth_draft"), status_code=303, fetch_redirect_response=False
        )

    @patch("app.services.auth.yandex_id.backend.requests.get")
    @patch("app.services.auth.yandex_id.backend.requests.post")
    def test_link_flow_creates_identity_for_current_user(self, mock_post, mock_get):
        current = User.objects.create_user(
            email="me@example.com", password="Password2025"
        )
        self.client.force_login(current)

        mock_post.return_value = SimpleNamespace(
            raise_for_status=lambda: None,
            json=lambda: {"access_token": "token123"},
        )
        mock_get.return_value = SimpleNamespace(
            raise_for_status=lambda: None,
            json=lambda: {
                "id": "ya-123",
                "default_email": None,
                "first_name": "Ivan",
                "last_name": "Ivanov",
            },
        )

        _ = self.client.get(reverse("yandex_auth") + "?link=1")
        state = self.client.session["oauth_state"]
        resp_cb = self.client.get(reverse("yandex_callback") + f"?state={state}&code=ok")
        self.assertEqual(resp_cb.status_code, 302)

        self.assertTrue(
            UserIdentity.objects.filter(
                provider="yandex", provider_user_id="ya-123", user=current
            ).exists()
        )
        self.assertEqual(int(self.client.session.get("_auth_user_id")), current.pk)

    @patch("app.services.auth.yandex_id.backend.requests.get")
    @patch("app.services.auth.yandex_id.backend.requests.post")
    def test_link_apply_updates_name(self, mock_post, mock_get):
        current = User.objects.create_user(
            email="me@example.com", password="Password2025"
        )
        self.client.force_login(current)

        mock_post.return_value = SimpleNamespace(
            raise_for_status=lambda: None,
            json=lambda: {"access_token": "token123"},
        )
        mock_get.return_value = SimpleNamespace(
            raise_for_status=lambda: None,
            json=lambda: {
                "id": "ya-999",
                "default_email": None,
                "first_name": "Ivan",
                "last_name": "Ivanov",
            },
        )

        # сначала линкуем провайдера (link=1)
        _ = self.client.get(reverse("yandex_auth") + "?link=1")
        state = self.client.session["oauth_state"]
        _ = self.client.get(reverse("yandex_callback") + f"?state={state}&code=ok")

        # затем обновляем данные (apply=1)
        _ = self.client.get(reverse("yandex_auth") + "?apply=1")
        state = self.client.session["oauth_state"]
        _ = self.client.get(reverse("yandex_callback") + f"?state={state}&code=ok")

        current.refresh_from_db()
        self.assertEqual((current.first_name, current.last_name), ("Ivan", "Ivanov"))
