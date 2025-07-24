import json
import re

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import Client, TestCase
from django.test.utils import override_settings
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .logic.tokens import account_activation_token

User = get_user_model()


DATA = {
        "email": "user123@example.com",
        "password": "Qwerty123",
        "passwordAgain": "Qwerty123",
        "acceptTerms": True
}


class BaseAuthTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get('/auth/csrf/')
        self.csrf_token = self.client.cookies['csrftoken'].value

    def register_user(self, client, data):
        token = self.csrf_token
        response = client.post(
            '/auth/register/',
            data=json.dumps(data),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=token
        )
        return response

    def activate_user(self, client, user):
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        response = client.get(f'/auth/activate/{uidb64}/{token}/')
        return response


class UsersTest(BaseAuthTest):
    def test_register_user_with_csrf(self):
        data = DATA
        response = self.register_user(self.client, data)

        self.assertEqual(
            response.content,
            b'{"status": "ok", "data": {"userId": 1}}'
        )

        self.assertNotEqual(
            response.status_code, 403,
            "CSRF check failed (403)"
        )

        self.assertIn(
            response.status_code, [200, 201],
            f"Unexpected status: {response.status_code}"
        )
        self.assertTrue(User.objects.filter(email=DATA["email"]).exists())

    @override_settings(
            EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
    )
    def test_email_is_send(self):
        data = DATA
        response = self.register_user(self.client, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Confirm registration', mail.outbox[0].subject)
        self.assertIn('To ensure registration', mail.outbox[0].body)
        self.assertIn('user123@example.com', mail.outbox[0].to)

    @override_settings(
            EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'
    )
    def test_user_activation_from_link_email(self):
        data = DATA
        response = self.register_user(self.client, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(mail.outbox), 1)

        body = mail.outbox[0].body
        match = re.search(r'/auth/activate/([\w-]+)/([\w\-]+)/', body)
        self.assertIsNotNone(match)

        uidb64, token = match.groups()

        activate_url = f'/auth/activate/{uidb64}/{token}/'
        activate_response = self.client.get(activate_url)

        self.assertIn(activate_response.status_code, [201, 302])
        user = User.objects.get(email=data["email"])
        self.assertTrue(user.is_active)

    def test_user_can_login_after_activation(self):
        data = DATA
        response = self.register_user(self.client, data)

        self.assertEqual(response.status_code, 201)

        user = User.objects.get(email=DATA["email"])
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        activation_response = self.client.get(
            f'/auth/activate/{uidb64}/{token}/'
        )
        self.assertIn(activation_response.status_code, [201, 302])
        user.refresh_from_db()
        self.assertTrue(user.is_active)

        login_data = {
            "email": DATA["email"],
            "password": DATA["password"]
        }

        response = self.client.post(
            '/auth/login/',
            data=json.dumps(login_data),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=self.csrf_token
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"status": "ok", "data": {"userId": 1}}'
        )
        self.assertIn("_auth_user_id", self.client.session)

    def test_user_can_logout_after_login(self):
        data = DATA
        response = self.register_user(self.client, data)

        self.assertEqual(response.status_code, 201)

        user = User.objects.get(email=DATA["email"])
        user.is_active = True
        user.save()
        user.refresh_from_db()
        self.assertTrue(user.is_active)

        login_data = {
            "email": DATA["email"],
            "password": DATA["password"]
        }

        response = self.client.post(
            '/auth/login/',
            data=json.dumps(login_data),
            content_type='application/json',
            HTTP_X_CSRFTOKEN=self.csrf_token
        )
        self.assertEqual(response.status_code, 200)

        self.client.get('/auth/csrf/')
        self.csrf_token = self.client.cookies['csrftoken'].value

        response = self.client.post(
            '/auth/logout/',
            content_type='application/json',
            HTTP_X_CSRFTOKEN=self.csrf_token
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content,
            b'{"status": "ok", "message": "User logged out"}'
        )
