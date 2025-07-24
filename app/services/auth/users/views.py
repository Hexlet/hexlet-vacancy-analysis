import logging

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from . import exceptions as custom_ex
from .logic.registration import register_user
from .logic.tokens import account_activation_token
from .logic.utils import read_data_from_request
from .logic.validators import normalize_email

User = get_user_model()

logger = logging.getLogger(__name__)


class CreateUserView(View):
    def get(self, request):
        pass

    def post(self, request):
        try:
            data = read_data_from_request(request)
            data["domain"] = get_current_site(request).domain
            result = register_user(data)
            return JsonResponse(
                {"status": "ok", "data": {"userId": result}},
                status=201
            )
        except custom_ex.ValidationError as e:
            logger.error(f"Validation Error: {e.message}")
            return e.to_response()

        except custom_ex.CreateUserError as e:
            logger.error(f"Error creating user: {e.message}")
            return e.to_response()

        except custom_ex.SendEmailError as e:
            logger.error(f"Error sending activation link: {e.message}")
            return e.to_response()

        except custom_ex.CustomBaseError as e:
            logger.error(f"Unknown error: {e.message}")
            return e.to_response()


class ActivateUser(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            logger.info(
                f"User '{user.email}' registration completed successfully"
            )
            return JsonResponse(
                {"status": "ok", "data": {"userId": uid}},
                status=201
            )
        else:
            return JsonResponse(
                {"status": "error", "message": "Activation link is invalid"},
                status=400
            )


class LoginUserView(View):
    def post(self, request):
        try:
            data = read_data_from_request(request)
        except custom_ex.ValidationError as e:
            logger.error(f"Validation Error: {e.message}")
            return e.to_response()

        email = normalize_email(data.get("email"))
        password = data.get("password")

        if not (email and password):
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Email and password required"
                }, status=400
            )

        user = authenticate(request, email=email, password=password)

        if user is None:
            return JsonResponse(
                {"status": "error", "message": "Invalid credential"},
                status=400
            )

        if not user.is_active:
            return JsonResponse(
                {"status": "error", "message": "User in not active"},
                status=400
            )

        login(request, user)
        return JsonResponse(
            {"status": "ok", "data": {"userId": user.id}}, status=200
        )


class LogoutUserView(View):
    def post(self, request):
        logout(request)
        return JsonResponse(
            {"status": "ok", "message": "User logged out"}, status=200
        )


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"message": "CSRF cookie set"})
