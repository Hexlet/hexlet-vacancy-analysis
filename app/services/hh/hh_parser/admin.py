from django.contrib import admin

from ...utils.main import custom_title_filter_factory
from .models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company__name",
        "city",
        "salary",
        "experience",
        "platform__name",
        "published_at",
    )
    search_fields = ("title", "company__name", "city__name", "platform__name", "skills")
    list_filter = (
        (
            "platform",
            custom_title_filter_factory(admin.RelatedFieldListFilter, "Platform"),
        ),
        "city",
        "experience",
        "schedule",
        "employment",
    )
    ordering = ("-published_at",)
    readonly_fields = ("created_at", "platform")

    fieldsets = (
        (
            "Description",
            {
                "fields": (
                    "platform",
                    "title",
                    "company",
                    "url",
                    "salary",
                    "experience",
                    "employment",
                    "work_format",
                    "schedule",
                    "skills",
                    "description",
                )
            },
        ),
        ("Location", {"fields": ("city", "address"), "classes": ("collapse",)}),
        (
            "Additional information",
            {
                "fields": ("contacts", "published_at", "created_at"),
                "classes": ("collapse",),
            },
        ),
    )