from django.contrib import admin

from .models import Region


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "code")
    search_fields = ("name", "code")
    list_filter = ("code",)
    ordering = ("name",)