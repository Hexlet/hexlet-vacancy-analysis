from inertia import share


class InertiaMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Делимся данными аутентификации со всеми компонентами
        share(
            request,
            auth={
                "user": {
                    "id": (
                        request.user.id
                        if request.user.is_authenticated
                        else None
                    ),
                    "username": (
                        request.user.username
                        if request.user.is_authenticated
                        else None
                    ),
                },
                "isAuthenticated": request.user.is_authenticated,
            },
        )

        response = self.get_response(request)
        return response