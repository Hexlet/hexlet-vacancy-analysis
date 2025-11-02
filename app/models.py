from django.core.exceptions import ValidationError
from django.db import models


class HomePageBlock(models.Model):
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

    class Meta:
        verbose_name = "Блок на главной странице"
        verbose_name_plural = "Блоки на главной странице"
        ordering = ["order"]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()

        if self.block_type == "hero":
            self._validate_hero_block()
        elif self.block_type == "stats":
            self._validate_stats_block()

    def _validate_hero_block(self):
        required_fields = ("heading", "subheading")
        for field in required_fields:
            if field not in self.content:
                raise ValidationError(
                    {"content": f"Hero  блок должен содержать поле: {field}"}
                )

    def _validate_stats_block(self):
        if "metrics" not in self.content:
            raise ValidationError(
                {"content": "Stats блок должен содержать список metrics"}
            )

        if not isinstance(self.content["metrics"], list):
            raise ValidationError({"content": "metrics должен быть списком"})
