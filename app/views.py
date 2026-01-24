from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
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
        status=500,
    )


def custom_not_found_error(request, exception):
    return JsonResponse(
        {"status": "error", "message": "Internal server error"},
        status=404,
    )


@require_GET
def robots_txt(request):
    """
    Генерирует текстовый файл robots.txt для управления поведением поисковых роботов.

    Формирует правила доступа к страницам сайта, указывая разрешенные и запрещенные пути,
    а также адрес карты сайта (sitemap.xml). Ответ возвращается в формате plain text.

    Parameters:
    ----------
    request : HttpRequest
        Объект HTTP-запроса (GET-метод). Используется для получения абсолютного URL
        карты сайта через метод `build_absolute_uri`.

    Returns:
    -------
    HttpResponse
        Текстовое содержимое файла robots.txt с заголовком `Content-Type: text/plain`.

    Notes:
    -----
    - Разрешенные пути (`Allow`) и запрещенные пути (`Disallow`) определяются списками
      `public_pages` и `private_pages`.
    - Адрес карты сайта (`Sitemap`) формируется динамически на основе текущего запроса.
    - Декоратор `@require_GET` гарантирует, что функция обрабатывает только GET-запросы.

    Example:
    -------
    При запросе `http://example.com/robots.txt` будет возвращён следующий текст:

    ```
    User-agent: *
    Allow:
    Disallow: /
    Disallow: /admin/
    Sitemap: http://example.com/sitemap.xml
    ```
    """
    public_pages = []

    private_pages = [
        "/",
        "/admin/",
    ]

    lines = [
        "User-agent: *",
        *[f"Allow: {page}" for page in public_pages],
        *[f"Disallow: {page}" for page in private_pages],
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
