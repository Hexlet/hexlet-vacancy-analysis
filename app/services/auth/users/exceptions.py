from django.http import JsonResponse


class CustomBaseError(Exception):
    default_message = "Server error"
    default_code = 500

    def __init__(self, message=None, code=None):
        super().__init__(message)
        self.message = message or self.default_message
        self.code = code or self.default_code

    def to_response(self):
        return JsonResponse(
            {"status": "error", "message": self.message}, status=self.code
        )


class ValidationError(CustomBaseError):
    pass


class CreateUserError(CustomBaseError):
    pass


class SendEmailError(CustomBaseError):
    pass
