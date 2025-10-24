from django.http import JsonResponse
from inertia import render as inertia_render


def index(request):
    return inertia_render(
        request,
        "HomePage",
        props={},
    )


def custom_server_error(request):
    return JsonResponse(
        {"status": "error", "message": "Internal server error"},
        status=500
    )


def custom_not_found_error(request, exception):
    return JsonResponse(
        {"status": "error", "message": "Internal server error"},
        status=404
    )

