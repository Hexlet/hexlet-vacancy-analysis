from typing import Any, Dict, Optional, Union

from django.http import HttpResponse
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme


def oauth_compute_next(request) -> Optional[str]:
    candidate_next = request.GET.get("next") or request.META.get("HTTP_REFERER")
    if candidate_next and url_has_allowed_host_and_scheme(
        url=candidate_next,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return candidate_next
    return None


def oauth_parse_apply_flag(request) -> bool:
    return (request.GET.get("apply") or "").lower() in ("1", "true", "yes")


def oauth_parse_link_flag(request) -> bool:
    return (request.GET.get("link") or "").lower() in ("1", "true", "yes")


def oauth_save_flow(
    request,
    state: str,
    next_url: Optional[str],
    apply_flag: bool,
    link_flag: bool = False,
) -> None:
    flows: Dict[str, Dict[str, Any]] = request.session.get("oauth_flows", {})
    flows[state] = {"next": next_url, "apply": apply_flag, "link": link_flag}
    request.session["oauth_flows"] = flows


def oauth_validate_state(request) -> Union[str, HttpResponse]:
    returned_state = request.GET.get("state")
    saved_state = request.session.pop("oauth_state", None)
    if not returned_state or returned_state != saved_state:
        return HttpResponse("Invalid OAuth state", status=400)
    return returned_state


def oauth_read_code(request) -> Union[str, HttpResponse]:
    code = request.GET.get("code")
    if not code:
        return HttpResponse("Ошибка: не передан code", status=400)
    return code


def oauth_pop_flow(request, state: str) -> Dict[str, Any]:
    flows: Dict[str, Dict[str, Any]] = request.session.get("oauth_flows", {})
    flow = flows.pop(state, {})
    request.session["oauth_flows"] = flows
    return flow


def oauth_resolve_next(
    request, candidate: Optional[str], fallback: str = "auth_draft"
) -> str:
    if candidate and url_has_allowed_host_and_scheme(
        url=candidate,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return candidate
    return reverse(fallback)


def oauth_apply_profile_if_requested(
    request, flow: Dict[str, Any], session_key: str
) -> None:
    if not flow.get("apply"):
        return
    suggested = request.session.get(session_key)
    if not (suggested and request.user.is_authenticated):
        return
    first_name = (suggested.get("first_name") or "").strip()
    last_name = (suggested.get("last_name") or "").strip()
    updates = {}
    if first_name and request.user.first_name != first_name:
        updates["first_name"] = first_name
    if last_name and request.user.last_name != last_name:
        updates["last_name"] = last_name
    if updates:
        for k, v in updates.items():
            setattr(request.user, k, v)
        request.user.save(update_fields=list(updates.keys()))
    request.session.pop(session_key, None)
