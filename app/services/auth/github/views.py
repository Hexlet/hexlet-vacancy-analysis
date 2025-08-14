import secrets
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.http import HttpResponse
from django.shortcuts import redirect, render

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
    """
    state = secrets.token_urlsafe(16)
    request.session["oauth_state"] = state

    params = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "redirect_uri": settings.GITHUB_REDIRECT_URI,
        "scope": "read:user user:email",
        "state": state,
    }
    url = "https://github.com/login/oauth/authorize?" + urlencode(params)
    return redirect(url)


def auth_callback(request):
    """
    обрабатывает callback от Github:
    валидирует state, вызывает GithubBackend через authenticate и логинит.
    """
    # проверка state и получение кода
    returned_state = request.GET.get("state")
    saved_state = request.session.pop("oauth_state", None)
    if not returned_state or returned_state != saved_state:
        return HttpResponse("Invalid OAuth state", status=400)

    code = request.GET.get("code")
    if not code:
        return HttpResponse("Ошибка: не передан code", status=400)

    # аутентификация через кастомный бэкенд
    user = authenticate(request, code=code)
    if user is None:
        return HttpResponse("Authentication failed", status=400)

    # логин и редирект обратно
    login(request, user)
    return redirect("github_login")
