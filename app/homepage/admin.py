import json

from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import HomePageBlock


class HomePageBlockForm(forms.ModelForm):
    class Meta:
        model = HomePageBlock
        fields = "__all__"
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 10, "style": "font-family: monospace;"}
            ),
        }

    def clean_content(self):
        content = self.cleaned_data["content"]
        if isinstance(content, str):
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                raise forms.ValidationError("Некоректный JSON формат")
        return content


@admin.register(HomePageBlock)
class HomePageBlockAdmin(admin.ModelAdmin):
    form = HomePageBlockForm

    list_display = (
        "title",
        "block_type_display",
        "order",
        "is_active",
        "preview_content",
    )
    search_fields = ("title", "description")
    list_filter = ("block_type", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)

    fieldsets = (
        (
            "Основная информация",
            {"fields": ("title", "description", "block_type", "order", "is_active")},
        ),
        (
            "Контент блока",
            {
                "fields": ("content",),
                "description": """Введите JSON структуру для блока. Пример для Hero: {
                        "heading": "Skill Pulse - Ваш гид на рынке IT-труда",
                        "subheading":
                            "Современная аналитическая платформа для
                            принятия взвешенных карьерных решений",
                        "cta_text": "Начать",
                        "cta_link": "/register",
                        "background_image": "/images/hero-bg.jpg"}""",
            },
        ),
    )

    def block_type_display(self, obj):
        return obj.get_block_type_display()

    block_type_display.short_description = "Тип блока"

    def preview_content(self, obj):
        return format_html('<code style="font-size: 1em;">{}</code>', obj.content)

    preview_content.short_description = "Контент"
