from django.core.exceptions import ValidationError


def validate_hero_block(self):
    """
    Валидирует содержимое блока типа 'hero'.

    Проверяет наличие обязательных полей в JSON-поле content.

    Args:
        self: Экземпляр модели HomePageBlock, для которого выполняется валидация.

    Raises:
        ValidationError: Если в content отсутствует одно из обязательных полей.
                         Ошибка связывается с полем 'content' и содержит
                         понятное сообщение о недостающем поле.
    """
    required_fields = ("heading", "subheading")
    for field in required_fields:
        if field not in self.content:
            raise ValidationError(
                {"content": f"Hero  блок должен содержать поле: {field}"}
            )


def validate_stats_block(self):
    """
    Валидирует содержимое блока типа 'stats'.

    Проверяет, что поле content содержит:
    1. Ключ 'metrics'
    2. Значение по ключу 'metrics' является списком (list)

    Args:
        self: Экземпляр модели HomePageBlock, для которого выполняется валидация.

    Raises:
        ValidationError: Если:
            - Отсутствует ключ 'metrics' в contt
            - Значение 'metrics' не является списком
    """
    if "metrics" not in self.content:
        raise ValidationError({"content": "Stats блок должен содержать список metrics"})

    if not isinstance(self.content["metrics"], list):
        raise ValidationError({"content": "metrics должен быть списком"})


VALIDATORS = {
    "hero": validate_hero_block,
    "stats": validate_stats_block,
}
