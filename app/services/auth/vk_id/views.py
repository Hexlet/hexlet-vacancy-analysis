import secrets
import requests
from urllib.parse import urlencode
import logging

from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.http import HttpResponse
from django.shortcuts import redirect
from inertia import inertia

User = get_user_model()
logger = logging.getLogger(__name__)


class VKOAuthError(Exception):
    """Custom exception for VK OAuth errors"""
    pass


def validate_state(request):
    state = request.GET.get("state")
    session_state = request.session.get("vk_state")
    
    if not state or state != session_state:
        logger.warning(f"Invalid state. Expected: {session_state}, Got: {state}")
        raise VKOAuthError("Invalid state parameter")
    
    request.session.pop("vk_state", None)
    logger.debug("State parameter validated")
    return True


def get_access_token(code: str) -> dict:
    params = {
        "client_id": settings.VK_CLIENT_ID,
        "client_secret": settings.VK_CLIENT_SECRET,
        "redirect_uri": settings.VK_REDIRECT_URI,
        "code": code,
    }

    try:
        res = requests.get("https://oauth.vk.com/access_token", params=params, timeout=10)
        res.raise_for_status()
        data = res.json()

        if "error" in data:
            raise VKOAuthError(f"VK token error: {data['error']}")
        return data

    except requests.Timeout:
        raise VKOAuthError("Timeout while connecting to VK")
    except requests.RequestException as e:
        logger.error(f"RequestException during token fetch: {e}")
        raise VKOAuthError(f"Failed to get VK access token: {str(e)}")


def get_vk_user_info(user_id: str, access_token: str) -> dict:
    params = {
        "user_ids": user_id,
        "fields": "first_name,last_name",
        "access_token": access_token,
        "v": "5.131",
    }

    try:
        res = requests.get("https://api.vk.com/method/users.get", params=params, timeout=10)
        res.raise_for_status()
        data = res.json()

        if "error" in data:
            raise VKOAuthError(f"VK API error: {data['error'].get('error_msg', 'Unknown error')}")
        if not data.get("response"):
            raise VKOAuthError("No user data in VK response")

        return data["response"][0]

    except requests.Timeout:
        raise VKOAuthError("Timeout while fetching VK user info")
    except requests.RequestException as e:
        raise VKOAuthError(f"Failed to fetch VK user info: {str(e)}")


def get_or_create_user(email: str, user_id: str, user_info: dict) -> User:
    if not email:
        email = f"vk_user_{user_id}@fake.vk.com"
        logger.debug(f"Generated fake email: {email}")

    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "username": f"vk_{user_id}",
            "first_name": user_info.get("first_name", ""),
            "last_name": user_info.get("last_name", ""),
        },
    )

    if created:
        user.set_unusable_password()
        user.save()
        logger.info(f"Created new user: {email}")
    else:
        logger.debug(f"Existing user found: {email}")

    return user


def vk_auth_callback(request):
    code = request.GET.get("code")
    if not code:
        return HttpResponse("Authorization code not provided", status=400)

    try:
        validate_state(request)
        token_data = get_access_token(code)
        access_token = token_data.get("access_token")
        email = token_data.get("email")
        user_id = token_data.get("user_id")

        if not access_token or not user_id:
            raise VKOAuthError("Missing access_token or user_id from VK")

        user_info = get_vk_user_info(user_id, access_token)
        user = get_or_create_user(email, user_id, user_info)

        login(request, user)
        logger.info(f"User {user.email} logged in via VK")

        redirect_url = getattr(settings, "LOGIN_REDIRECT_URL", "/")
        return inertia.redirect(request, redirect_url)

    except VKOAuthError as e:
        logger.error(f"VK OAuth error: {str(e)}")
        return HttpResponse(str(e), status=400)
    except (requests.RequestException, requests.Timeout) as e:
        logger.error(f"VK API request failed: {str(e)}")
        return HttpResponse(f"VK API error: {str(e)}", status=400)
