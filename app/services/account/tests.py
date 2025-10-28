import json

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class ProfileEditViewTests(TestCase):
    def setUp(self):
        self.url = reverse("account_profile_edit")
        User = get_user_model()
        self.user = User.objects.create_user(
            email="user@example.com", password="pass123", first_name="", last_name=""
        )

    def test_get_inertia_authenticated_returns_props(self):
        self.client.force_login(self.user)
        resp = self.client.get(self.url, HTTP_X_INERTIA="true")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp["X-Inertia"], "true")
        self.assertIn("application/json", resp["Content-Type"])
        data = json.loads(resp.content)
        self.assertEqual(data.get("component"), "ProfileEdit")
        self.assertEqual(data.get("props", {}).get("email"), self.user.email)

    def test_get_inertia_unauthenticated_returns_401(self):
        resp = self.client.get(self.url, HTTP_X_INERTIA="true")
        self.assertEqual(resp.status_code, 401)
        data = json.loads(resp.content)
        self.assertEqual(data.get("status"), "error")

    def test_post_inertia_validation_errors_status_422(self):
        self.client.force_login(self.user)
        too_long = "x" * 151
        resp = self.client.post(
            self.url,
            {"first_name": too_long, "last_name": "Ok"},
            HTTP_X_INERTIA="true",
        )
        self.assertEqual(resp.status_code, 422)
        data = json.loads(resp.content)
        props = data.get("props", {})
        self.assertIn("errors", props)
        self.assertIn("first_name", props["errors"])

    def test_post_inertia_success_redirects_303_and_updates(self):
        self.client.force_login(self.user)
        resp = self.client.post(
            self.url,
            {"first_name": "Ivan", "last_name": "Petrov", "next": "/welcome/"},
            HTTP_X_INERTIA="true",
        )
        self.assertEqual(resp.status_code, 303)
        self.assertEqual(resp["Location"], "/welcome/")
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Ivan")
        self.assertEqual(self.user.last_name, "Petrov")

    def test_post_success_redirects_to_profile_when_next_invalid(self):
        self.client.force_login(self.user)
        resp = self.client.post(
            self.url,
            {"first_name": "Ivan", "last_name": "Petrov", "next": "https://ya.ru/"},
        )
        self.assertEqual(resp.status_code, 303)
        self.assertEqual(resp["Location"], reverse("account_profile_edit"))

    def test_post_inertia_update_phone_success(self):
        self.client.force_login(self.user)
        resp = self.client.post(
            self.url,
            {"first_name": "", "last_name": "", "phone": "8" + "9991234567"},
            HTTP_X_INERTIA="true",
        )
        self.assertEqual(resp.status_code, 303)
        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, "+79991234567")

    def test_post_inertia_phone_invalid(self):
        self.client.force_login(self.user)
        resp = self.client.post(
            self.url,
            {"first_name": "", "last_name": "", "phone": "123"},
            HTTP_X_INERTIA="true",
        )
        self.assertEqual(resp.status_code, 422)
        data = json.loads(resp.content)
        props = data.get("props", {})
        self.assertIn("errors", props)
        self.assertIn("phone", props["errors"])

    def test_post_inertia_phone_duplicate(self):
        # другой пользователь с этим же телефоном
        U = get_user_model()
        U.objects.create_user(
            email="another@example.com", password="pass123", phone="+79991234567"
        )
        self.client.force_login(self.user)
        resp = self.client.post(
            self.url,
            {"first_name": "", "last_name": "", "phone": "+79991234567"},
            HTTP_X_INERTIA="true",
        )
        self.assertEqual(resp.status_code, 422)
        data = json.loads(resp.content)
        props = data.get("props", {})
        self.assertIn("errors", props)
        self.assertEqual(props["errors"].get("phone"), "Phone already in use")
