import secrets
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from inertia import location

from app.services.auth.users import exceptions as custom_ex
from app.services.auth.users.logic.registration import register_user
from app.services.auth.users.logic.validators import normalize_email

User = get_user_model()


def draft_login(request):
    """
    Рендерит страницу с кнопкой входа через Github и показывает данные пользователя,
    если он залогинен.
    """
    context = {}
    if request.user.is_authenticated:
        context["github_user"] = {
            "email": request.user.email,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
        }
    return render(request, "github/draft_github_auth.html", context)


def start_auth(request):
    """
    Генерирует state, сохраняет его в сессии и
    перенаправляет пользователя на страницу авторизации Github.
    + Запоминаем, откуда стартовали (next), и поддерживаем Inertia-визит.
    """

    state = secrets.token_urlsafe(16)
    request.session["oauth_state"] = state

    # откуда вернуться
    candidate_next = request.GET.get("next") or request.META.get("HTTP_REFERER")
    is_valid_next = bool(
        candidate_next
        and url_has_allowed_host_and_scheme(
            url=candidate_next,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        )
    )
    next_url = candidate_next if is_valid_next else None

    # привязка next к state для нескольких вкладок
    flows = request.session.get("oauth_flows", {})
    flows[state] = {"next": next_url}
    request.session["oauth_flows"] = flows

    # адрес авторизации
    params = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "redirect_uri": settings.GITHUB_REDIRECT_URI,
        "scope": "read:user user:email",
        "state": state,
    }
    url = "https://github.com/login/oauth/authorize?" + urlencode(params)

    # если вход со страницы с Inertia - 409 + X-Inertia-Location
    if request.headers.get("X-Inertia"):
        return location(url)

    return redirect(url)


def auth_callback(request):
    """
    Обрабатывает callback от Github:
    валидирует state, вызывает GithubBackend через authenticate и логинит.
    + Возвращаемся на сохранённый next (если валиден).
    """

    # проверка state
    returned_state = request.GET.get("state")
    saved_state = request.session.pop("oauth_state", None)
    if not returned_state or returned_state != saved_state:
        return HttpResponse("Invalid OAuth state", status=400)

    # чтение code
    code = request.GET.get("code")
    if not code:
        return HttpResponse("Ошибка: не передан code", status=400)

    # ауф через свой backend
    user = authenticate(request, code=code)
    if user is None:
        return HttpResponse("Authentication failed", status=400)

    # непосредственно логин
    login(request, user)

    # достаем сохранённый next именно для этого state
    flows = request.session.get("oauth_flows", {})
    flow = flows.pop(returned_state, {})  # удаляем, чтобы одноразово
    request.session["oauth_flows"] = flows
    next_url = flow.get("next")

    # редирект
    if not (
        next_url
        and url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        )
    ):
        next_url = reverse("github_login")

    return redirect(next_url)


@require_POST
def email_register(request):
    """
    Вызывает register_user для html форм.
    """
    email = (request.POST.get("email") or "").strip()
    password = request.POST.get("password") or ""
    password_again = request.POST.get("passwordAgain") or ""
    accept = request.POST.get("acceptTerms") in ("on", "true", "1", True)

    data = {
        "email": email,
        "password": password,
        "passwordAgain": password_again,
        "acceptTerms": accept,
        "domain": get_current_site(request).domain,
    }

    try:
        _user_id = register_user(data)
        messages.success(request, "Регистрация прошла. Проверьте почту для активации.")
    except custom_ex.ValidationError as e:
        messages.error(request, e.message)
    except custom_ex.CreateUserError as e:
        messages.error(request, e.message)
    except custom_ex.SendEmailError as e:
        messages.error(request, e.message)
    except custom_ex.CustomBaseError as e:
        messages.error(request, e.message)

    return redirect("github_login")


@require_POST
def email_login(request):
    """
    логинит по почте (EmailAuthBackend).
    """
    email = normalize_email(request.POST.get("email") or "")
    password = request.POST.get("password") or ""

    if not (email and password):
        messages.error(request, "Email and password required")
        return redirect("github_login")

    user = authenticate(request, email=email, password=password)
    if user is None:
        messages.error(request, "Invalid credential")
        return redirect("github_login")

    if not getattr(user, "is_active", False):
        messages.error(request, "User in not active")
        return redirect("github_login")

    login(request, user)
    messages.success(request, "Вход выполнен.")
    return redirect("github_login")
