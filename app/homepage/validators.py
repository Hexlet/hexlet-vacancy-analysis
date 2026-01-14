from typing import Any

from django.core.exceptions import ValidationError

# Константы для обязательных полей
HERO_REQUIRED_FIELDS = ("heading", "subheading")
STATS_REQUIRED_FIELDS = ("metrics",)

# Константы для сообщений об ошибках
ERROR_MESSAGES = {
    "hero_missing_field": "Hero блок должен содержать поле: {field}",
    "stats_missing_metrics": "Stats блок должен содержать ключ 'metrics'",
    "stats_metrics_not_list": "Поле 'metrics' должно быть списком",
    "invalid_content_type": "Содержимое должно быть объектом JSON",
}


def validate_required_fields(
    content: Any,
    required_fields: tuple[str, ...],
    error_key: str,
) -> None:
    """
    Проверяет наличие обязательных полей в словаре.

    Args:
        content: Содержимое для проверки.
        required_fields: Кортеж обязательных полей.
        error_key: Ключ для получения сообщения об ошибке из ERROR_MESSAGES.

    Raises:
        ValidationError: Если содержимое не является словарём
            или отсутствует обязательное поле.
    """
    if not isinstance(content, dict):
        raise ValidationError({"content": ERROR_MESSAGES["invalid_content_type"]})

    for field in required_fields:
        if field not in content:
            raise ValidationError(
                {"content": ERROR_MESSAGES[error_key].format(field=field)}
            )


def validate_hero_block(self: Any) -> None:
    """
    Валидирует содержимое блока типа 'hero'.

    Проверяет наличие обязательных полей (heading, subheading) в JSON-поле content.

    Args:
        self: Экземпляр модели HomePageBlock, для которого выполняется валидация.

    Raises:
        ValidationError: Если в content отсутствует одно из обязательных полей.
    """
    validate_required_fields(self.content, HERO_REQUIRED_FIELDS, "hero_missing_field")


def validate_stats_block(self: Any) -> None:
    """
    Валидирует содержимое блока типа 'stats'.

    Проверяет, что поле content содержит:
    1. Ключ 'metrics'
    2. Значение по ключу 'metrics' является списком (list)

    Args:
        self: Экземпляр модели HomePageBlock, для которого выполняется валидация.

    Raises:
        ValidationError: Если:
            - Содержимое не является словарём
            - Отсутствует ключ 'metrics'
            - Значение 'metrics' не является списком
    """
    validate_required_fields(
        self.content, STATS_REQUIRED_FIELDS, "stats_missing_metrics"
    )

    if not isinstance(self.content["metrics"], list):
        raise ValidationError({"content": ERROR_MESSAGES["stats_metrics_not_list"]})


VALIDATORS = {
    "hero": validate_hero_block,
    "stats": validate_stats_block,
}
