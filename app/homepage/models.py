from django.db import models

from .validators import VALIDATORS


class HomePageBlockQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def ordered(self):
        return self.order_by("order")

    def for_homepage(self):
        return (
            self.active()
            .ordered()
            .values("id", "title", "block_type", "content", "order")
        )


class HomePageBlock(models.Model):
    """
    Модель блока для главной страницы сайта.

    Представляет собой гибкий компонент контента, который может иметь разные типы
    и структуру в зависимости от назначения.

    Используется для построения главной страницы из независимых блоков,
    таких как главный раздел, статистика и другие.

    Атрибуты:
        BLOCK_TYPES (tuple): Доступные типы блоков с их отображаемыми названиями.
    """

    BLOCK_TYPES = (
        ("hero", "Главный раздел"),
        ("stats", "Статистика"),
    )

    title = models.CharField(max_length=50, verbose_name="Название блока")
    description = models.TextField(blank=True, verbose_name="Описание")
    content = models.JSONField(default=dict, verbose_name="JSON контент")
    block_type = models.CharField(
        max_length=50, choices=BLOCK_TYPES, verbose_name="Тип блока"
    )
    order = models.IntegerField(default=0, verbose_name="Порядок")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    objects = HomePageBlockQuerySet.as_manager()

    class Meta:
        verbose_name = "Блок на главной странице"
        verbose_name_plural = "Блоки на главной странице"
        ordering = ["order"]

    def __str__(self):
        return self.title

    def clean(self):
        """
        Выполняет валидацию модели перед сохранением.

        Raises:
            ValidationError: Если данные не проходят валидацию в вызванной функции.
        """
        super().clean()

        validators = VALIDATORS.get(self.block_type)
        if validators:
            validators(self)
