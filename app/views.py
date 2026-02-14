from django.http import JsonResponse


def custom_server_error(request):
    return JsonResponse(
        {"status": "error", "message": "Internal server error"}, status=500
    )


def custom_not_found_error(request, exception):
    return JsonResponse(
        {"status": "error", "message": "Internal server error"}, status=404
    )
