from django.contrib import admin
from .models import Vacancy


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'company_name',
        'city',
        'salary',
        'experience',
        'published_at',
    )
    search_fields = ('title', 'company_name', 'city', 'key_skills')
    list_filter = ('city', 'experience', 'schedule', 'employment')
    ordering = ('-published_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Description', {
            'fields': (
                'title', 'company_name', 'url', 'salary', 'experience',
                'employment', 'work_format', 'schedule', 'key_skills', 'description',
            )
        }),
        ('Lokation', {
            'fields': ('city', 'street', 'building'),
            'classes': ('collapse',)
        }),
        ('Additional information', {
            'fields': ('contacts', 'published_at', 'created_at'),
            'classes': ('collapse',)
        }),
    )
