from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import resolve, reverse

from app.services.auth.github import views
from app.services.auth.users import exceptions as custom_ex

User = get_user_model()


class GithubURLTests(TestCase):
    """
    проверяем, что маршруты и имена URL-ов корректны.
    """

    def test_urls_resolve(self):
        self.assertEqual(resolve("/auth/github/").func, views.draft_login)
        self.assertEqual(resolve("/auth/github/start/").func, views.start_auth)
        self.assertEqual(resolve("/auth/github/callback/").func, views.auth_callback)
        # адаптеры форм
        self.assertEqual(
            resolve("/auth/github/email/register/").func.__name__, "email_register"
        )
        self.assertEqual(
            resolve("/auth/github/email/login/").func.__name__, "email_login"
        )

    def test_reverse_names(self):
        self.assertEqual(reverse("github_login"), "/auth/github/")
        self.assertEqual(reverse("github_auth"), "/auth/github/start/")
        self.assertEqual(reverse("github_callback"), "/auth/github/callback/")
        self.assertEqual(
            reverse("github_email_register"), "/auth/github/email/register/"
        )
        self.assertEqual(reverse("github_email_login"), "/auth/github/email/login/")


class GithubViewsTests(TestCase):
    """
    проверки draft-страницы, старта OAuth, callback-а, email-форм и логики next.
    """

    def setUp(self):
        self.client = Client()

    # ----- draft_login ------------------------------------------------------

    def test_draft_login_shows_link(self):
        resp = self.client.get(reverse("github_login"))
        self.assertContains(resp, "Войти через GitHub")

    # ----- start_auth (обычный визит, 302) ---------------------------------

    def test_start_auth_redirects_and_sets_state(self):
        resp = self.client.get(reverse("github_auth"))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(
            resp["Location"].startswith("https://github.com/login/oauth/authorize"),
            resp["Location"],
        )
        # state должен появиться в сессии
        self.assertIn("oauth_state", self.client.session)
        # и должна существовать карта oauth_flows, где есть ключ для этого state
        state = self.client.session["oauth_state"]
        flows = self.client.session.get("oauth_flows", {})
        self.assertIn(state, flows)
        self.assertIn("next", flows[state])
        self.assertIsNone(flows[state]["next"])

    def test_start_auth_stores_valid_next_from_query(self):
        resp = self.client.get(reverse("github_auth") + "?next=/some/path")
        self.assertEqual(resp.status_code, 302)
        state = self.client.session["oauth_state"]
        flows = self.client.session.get("oauth_flows", {})
        self.assertEqual(flows[state]["next"], "/some/path")

    def test_start_auth_ignores_external_next(self):
        resp = self.client.get(reverse("github_auth") + "?next=https://evil.com/steal")
        self.assertEqual(resp.status_code, 302)
        state = self.client.session["oauth_state"]
        flows = self.client.session.get("oauth_flows", {})
        # внешний next должен быть отфильтрован
        self.assertIsNone(flows[state]["next"])

    def test_start_auth_uses_referer_when_no_next(self):
        resp = self.client.get(
            reverse("github_auth"),
            # реферер на свой относительный путь должен пройти валидацию
            **{"HTTP_REFERER": "/from/page"},
        )
        self.assertEqual(resp.status_code, 302)
        state = self.client.session["oauth_state"]
        flows = self.client.session.get("oauth_flows", {})
        self.assertEqual(flows[state]["next"], "/from/page")

    # ----- auth_callback: невалидный state ----------------------------------

    def test_auth_callback_invalid_state(self):
        url = reverse("github_callback") + "?state=wrong&code=any"
        resp = self.client.get(url)
        self.assertContains(resp, "Invalid OAuth state", status_code=400)

    # ----- auth_callback: backend вернул None -------------------------------

    def test_auth_callback_authentication_failed(self):
        """
        если GithubBackend ничего не вернул, получаем 400.
        """
        # сначала запрашиваем старт, чтобы появился правильный state
        _ = self.client.get(reverse("github_auth"))
        state = self.client.session["oauth_state"]

        with patch("app.services.auth.github.views.authenticate", return_value=None):
            resp = self.client.get(
                reverse("github_callback") + f"?state={state}&code=badcode"
            )
        self.assertContains(resp, "Authentication failed", status_code=400)

    # ----- auth_callback: успешный OAuth-flow -------------------------------

    @patch("app.services.auth.github.backend.requests.get")
    @patch("app.services.auth.github.backend.requests.post")
    def test_full_oauth_flow(self, mock_post, mock_get):
        """
        проверяем happy-path: обмен code -> token, получение профиля,
        сохранение пользователя, логин и редирект (без next -> на github_login).
        """
        # мокаем запрос code  ->  token
        mock_post.return_value = SimpleNamespace(
            raise_for_status=lambda: None,
            json=lambda: {"access_token": "gh_token"},
        )

        # мокаем запрос профиля
        def _mock_get(url, *args, **kwargs):
            if url.endswith("/user"):
                return SimpleNamespace(
                    raise_for_status=lambda: None,
                    json=lambda: {"login": "octocat", "name": "Octo Cat", "email": None},
                )
            elif url.endswith("/user/emails"):
                return SimpleNamespace(
                    raise_for_status=lambda: None,
                    json=lambda: [
                        {"email": "octo@example.com", "verified": True, "primary": True}
                    ],
                )
            raise AssertionError("Unexpected URL " + url)

        mock_get.side_effect = _mock_get

        # генерируем state (start_auth) — чтобы прошла проверка
        resp_start = self.client.get(reverse("github_auth"))
        self.assertEqual(resp_start.status_code, 302)
        state = self.client.session["oauth_state"]

        # вызываем callback с правильным state & любым code
        resp_cb = self.client.get(
            reverse("github_callback") + f"?state={state}&code=abc"
        )
        self.assertRedirects(resp_cb, reverse("github_login"))

        # убеждаемся, что пользователь создан и данные записаны
        user = User.objects.get(email="octo@example.com")
        self.assertEqual((user.first_name, user.last_name), ("Octo", "Cat"))

    # ----- auth_callback: возврат на next -----------------------------------

    def test_auth_callback_redirects_to_next_and_cleans_flow(self):
        """
        стартуем с валидным next, затем колбэк редиректит туда же,
        а запись в flows удаляется.
        """
        # старт с next
        resp_start = self.client.get(reverse("github_auth") + "?next=/welcome")
        self.assertEqual(resp_start.status_code, 302)
        state = self.client.session["oauth_state"]
        self.assertEqual(self.client.session["oauth_flows"][state]["next"], "/welcome")

        # готовим пользователя и удачную authenticate
        user = User.objects.create_user(email="u@example.com", password="Password2025")
        user.backend = "django.contrib.auth.backends.ModelBackend"
        with patch("app.services.auth.github.views.authenticate", return_value=user):
            resp_cb = self.client.get(
                reverse("github_callback") + f"?state={state}&code=ok"
            )

        self.assertRedirects(resp_cb, "/welcome", fetch_redirect_response=False)

        # запись по state должна быть удалена (одноразовость)
        flows = self.client.session.get("oauth_flows", {})
        self.assertNotIn(state, flows)

    def test_auth_callback_with_bad_next_falls_back(self):
        """
        стартуем с внешним next -> он игнорируется, после колбэка редирект на дефолт.
        """
        # внешний next отфильтруется уже на старте
        _ = self.client.get(reverse("github_auth") + "?next=https://evil.com/path")
        state = self.client.session["oauth_state"]

        user = User.objects.create_user(email="x@example.com", password="Password2025")
        user.backend = "django.contrib.auth.backends.ModelBackend"
        with patch("app.services.auth.github.views.authenticate", return_value=user):
            resp_cb = self.client.get(
                reverse("github_callback") + f"?state={state}&code=ok"
            )
        self.assertRedirects(resp_cb, reverse("github_login"))

    # ----- регистрация ------------------------------------------------------

    def test_email_register_get_not_allowed(self):
        resp = self.client.get(reverse("github_email_register"))
        self.assertEqual(resp.status_code, 405)  # require_POST

    @patch("app.services.auth.github.views.register_user")
    def test_email_register_success(self, mock_register):
        mock_register.return_value = 42  # user id
        resp = self.client.post(
            reverse("github_email_register"),
            data={
                "email": "user@example.com",
                "password": "Password2025",
                "passwordAgain": "Password2025",
                "acceptTerms": "on",
            },
        )
        self.assertRedirects(resp, reverse("github_login"))

    @patch("app.services.auth.github.views.register_user")
    def test_email_register_validation_error(self, mock_register):
        mock_register.side_effect = custom_ex.ValidationError("bad input")
        resp = self.client.post(
            reverse("github_email_register"),
            data={
                "email": "bad",
                "password": "123",
                "passwordAgain": "456",
                "acceptTerms": "on",
            },
        )
        self.assertRedirects(resp, reverse("github_login"))

    # ----- вход по email ----------------------------------------------------

    def test_email_login_get_not_allowed(self):
        resp = self.client.get(reverse("github_email_login"))
        self.assertEqual(resp.status_code, 405)

    def test_email_login_success(self):
        user = User.objects.create_user(
            email="user@example.com", password="Password2025"
        )
        self.assertTrue(user.is_active)

        resp = self.client.post(
            reverse("github_email_login"),
            data={"email": "user@example.com", "password": "Password2025"},
        )
        self.assertRedirects(resp, reverse("github_login"))
        # после логина сессия содержит _auth_user_id
        self.assertEqual(int(self.client.session.get("_auth_user_id")), user.pk)

    def test_email_login_invalid_credentials(self):
        User.objects.create_user(email="user@example.com", password="Password2025")
        resp = self.client.post(
            reverse("github_email_login"),
            data={"email": "user@example.com", "password": "wrong"},
        )
        self.assertRedirects(resp, reverse("github_login"))
        self.assertIsNone(self.client.session.get("_auth_user_id"))

    def test_email_login_inactive_user(self):
        # неактивный пользователь не должен логиниться
        user = User.objects.create_user(
            email="inactive@example.com", password="Password2025"
        )
        user.is_active = False
        user.save(update_fields=["is_active"])

        resp = self.client.post(
            reverse("github_email_login"),
            data={"email": "inactive@example.com", "password": "Password2025"},
        )
        self.assertRedirects(resp, reverse("github_login"))
        self.assertIsNone(self.client.session.get("_auth_user_id"))
