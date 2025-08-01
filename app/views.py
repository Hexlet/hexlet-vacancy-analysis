from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.http import require_GET


def custom_server_error(request):
    return JsonResponse(
        {"status": "error", "message": "Internal server error"}, status=500
    )


def custom_not_found_error(request, exception):
    return JsonResponse(
        {"status": "error", "message": "Internal server error"}, status=404
    )


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Allow: /",
        "Disallow: /admin",
        "Disallow: /auth",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
