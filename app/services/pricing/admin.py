from django.contrib import admin

from .models import PlanFeature, PricingPlan


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "currency", "period", "is_active", "order")
    list_editable = ("price", "period", "is_active")
    filter_horizontal = ("features",)


@admin.register(PlanFeature)
class PlanFeatureAdmin(admin.ModelAdmin):
    list_display = ("name",)
