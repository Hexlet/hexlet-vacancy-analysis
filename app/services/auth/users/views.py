import logging

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from . import exceptions as custom_ex
from .logic.registration import register_user
from .logic.tokens import account_activation_token
from .logic.utils import read_data_from_request
from .logic.validators import normalize_email

User = get_user_model()

logger = logging.getLogger(__name__)


def draft_auth(request):
    """
    Черновая страница авторизации: кнопка Яндекс и формы e-mail.
    """
    context = {}
    if request.user.is_authenticated:
        context["user_info"] = {
            "email": request.user.email,
            "first_name": getattr(request.user, "first_name", ""),
            "last_name": getattr(request.user, "last_name", ""),
        }
        # список подключённых провайдеров
        try:
            identities = list(request.user.identities.all())
            providers = {i.provider for i in identities}
            context["linked"] = {
                "github": "github" in providers,
                "yandex": "yandex" in providers,
            }
        except Exception:
            context["linked"] = {"github": False, "yandex": False}

    return render(request, "users/draft_auth.html", context)


def apply_yandex_profile(request):
    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "message": "Method not allowed"}, status=405
        )
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "error", "message": "Authentication required"}, status=401
        )

    suggested = request.session.get("yandex_profile_suggested")
    if not suggested:
        return JsonResponse(
            {"status": "error", "message": "No suggested data"}, status=404
        )

    first_name = (suggested.get("first_name") or "").strip()
    last_name = (suggested.get("last_name") or "").strip()

    user = request.user
    updates = {}
    if first_name and user.first_name != first_name:
        updates["first_name"] = first_name
    if last_name and user.last_name != last_name:
        updates["last_name"] = last_name

    if updates:
        for k, v in updates.items():
            setattr(user, k, v)
        user.save(update_fields=list(updates.keys()))

    try:
        del request.session["yandex_profile_suggested"]
    except KeyError:
        pass

    return JsonResponse({"status": "ok", "data": {"updated": list(updates.keys())}})


def apply_github_profile(request):
    if request.method != "POST":
        return JsonResponse(
            {"status": "error", "message": "Method not allowed"}, status=405
        )
    if not request.user.is_authenticated:
        return JsonResponse(
            {"status": "error", "message": "Authentication required"}, status=401
        )

    suggested = request.session.get("github_profile_suggested")
    if not suggested:
        return JsonResponse(
            {"status": "error", "message": "No suggested data"}, status=404
        )

    first_name = (suggested.get("first_name") or "").strip()
    last_name = (suggested.get("last_name") or "").strip()

    user = request.user
    updates = {}
    if first_name and user.first_name != first_name:
        updates["first_name"] = first_name
    if last_name and user.last_name != last_name:
        updates["last_name"] = last_name

    if updates:
        for k, v in updates.items():
            setattr(user, k, v)
        user.save(update_fields=list(updates.keys()))

    request.session.pop("github_profile_suggested", None)

    return JsonResponse({"status": "ok", "data": {"updated": list(updates.keys())}})


class CreateUserView(View):
    def get(self, request):
        pass

    def post(self, request):
        try:
            data = read_data_from_request(request)
            data["domain"] = get_current_site(request).domain
            result = register_user(data)
            return JsonResponse({"status": "ok", "data": {"userId": result}}, status=201)
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
            logger.info(f"User '{user.email}' registration completed successfully")
            return JsonResponse({"status": "ok", "data": {"userId": uid}}, status=201)
        else:
            return JsonResponse(
                {"status": "error", "message": "Activation link is invalid"}, status=400
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
                {"status": "error", "message": "Email and password required"}, status=400
            )

        user = authenticate(request, email=email, password=password)

        if user is None:
            return JsonResponse(
                {"status": "error", "message": "Invalid credential"}, status=400
            )

        if not user.is_active:
            return JsonResponse(
                {"status": "error", "message": "User in not active"}, status=400
            )

        login(request, user)
        return JsonResponse({"status": "ok", "data": {"userId": user.id}}, status=200)


class LogoutUserView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({"status": "ok", "message": "User logged out"}, status=200)


def _unlink_provider(request, provider: str):
    if not request.user.is_authenticated:
        messages.error(request, "Нужна авторизация")
        resp = redirect(reverse("auth_draft"))
        resp.status_code = 303
        return resp

    user = request.user
    identity = getattr(user, "identities", None)
    identity = identity.filter(provider=provider).first() if identity else None

    if not identity:
        messages.info(request, "Провайдер не подключён")
        resp = redirect(reverse("auth_draft"))
        resp.status_code = 303
        return resp

    other_count = user.identities.exclude(provider=provider).count()
    if other_count == 0 and not user.has_usable_password():
        messages.error(
            request,
            """Нельзя отключить последний способ входа.
            Установите пароль или подключите другой провайдер.""",
        )
        resp = redirect(reverse("auth_draft"))
        resp.status_code = 303
        return resp

    identity.delete()
    messages.success(request, "Провайдер отключён")
    resp = redirect(reverse("auth_draft"))
    resp.status_code = 303
    return resp


@require_POST
def unlink_github(request):
    return _unlink_provider(request, "github")


@require_POST
def unlink_yandex(request):
    return _unlink_provider(request, "yandex")


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"message": "CSRF cookie set"})
