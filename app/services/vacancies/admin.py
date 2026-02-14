from django.contrib import admin

from .models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "city",
        "salary",
        "experience",
        "platform",
        "published_at",
    )
    search_fields = (
        "title",
        "company__name",
        "city__name",
        "platform",
        "skills",
    )
    list_filter = (
        "platform",
        "city",
        "experience",
        "schedule",
        "employment",
    )
    ordering = ("-published_at",)
    readonly_fields = (
        "platform",
        "title",
        "company",
        "city",
        "address",
        "url",
        "salary",
        "experience",
        "employment",
        "work_format",
        "schedule",
        "skills",
        "description",
        "created_at",
        "published_at",
    )

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