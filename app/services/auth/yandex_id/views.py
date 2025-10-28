import secrets
from urllib.parse import urlencode

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from inertia import location

from app.services.auth.common import (
    oauth_apply_profile_if_requested,
    oauth_compute_next,
    oauth_parse_apply_flag,
    oauth_parse_link_flag,
    oauth_pop_flow,
    oauth_read_code,
    oauth_resolve_next,
    oauth_validate_state,
)

User = get_user_model()


def start_auth(request):
    """
    Генерирует state, сохраняет его в сессии и
    перенаправляет пользователя на страницу авторизации Яндекс.
    + Запоминаем, откуда стартовали (next), и поддерживаем Inertia-визит.
    """
    state = secrets.token_urlsafe(16)
    request.session["oauth_state"] = state

    # откуда вернуться
    next_url = oauth_compute_next(request)

    # флаги apply/link
    from app.services.auth.common import oauth_save_flow

    apply_flag = oauth_parse_apply_flag(request)
    link_flag = oauth_parse_link_flag(request)

    # если запросили apply, но провайдер не подключён — запрещаем
    if apply_flag and request.user.is_authenticated:
        identities = getattr(request.user, "identities", None)
        is_linked = (
            bool(identities.filter(provider="yandex").exists()) if identities else False
        )
        if not is_linked:
            messages.error(
                request, "Сначала подключите Yandex ID, затем обновляйте данные."
            )
            resp = redirect(reverse("auth_draft"))
            resp.status_code = 303
            return resp

    oauth_save_flow(request, state, next_url, apply_flag, link_flag)

    # адрес авторизации
    params = {
        "response_type": "code",
        "client_id": settings.YANDEX_CLIENT_ID,
        "redirect_uri": settings.YANDEX_REDIRECT_URI,
        "state": state,
        "scope": "login:email login:info",
    }
    url = "https://oauth.yandex.ru/authorize?" + urlencode(params)

    # если вход со страницы с Inertia - 409 + X-Inertia-Location
    if request.headers.get("X-Inertia"):
        return location(url)
    return redirect(url)


def auth_callback(request):
    """
    обрабатывает callback от Яндекса:
    валидирует state, вызывает YandexBackend через authenticate и логинит.
    + Возвращаемся на сохранённый next (если валиден).
    """
    # проверка state
    result = oauth_validate_state(request)
    if isinstance(result, HttpResponse):
        return result
    returned_state = result

    # чтение code
    result = oauth_read_code(request)
    if isinstance(result, HttpResponse):
        return result
    code = result

    # link-flow: привязка провайдера к текущему пользователю
    flow_peek = request.session.get("oauth_flows", {}).get(returned_state, {})
    link_user = (
        request.user
        if (flow_peek.get("link") and request.user.is_authenticated)
        else None
    )

    # ауф через свой backend
    user = authenticate(request, code=code, link_to_user=link_user, provider="yandex")
    if user is None:
        return HttpResponse("Authentication failed", status=400)

    # непосредственно логин
    login(request, user)

    # достаем сохранённый next и флаги именно для этого state
    flow = oauth_pop_flow(request, returned_state)
    next_url = oauth_resolve_next(request, flow.get("next"))
    oauth_apply_profile_if_requested(request, flow, "yandex_profile_suggested")
    return redirect(next_url)
