from django.contrib import admin

from .models import AgencyPlanFeature, AgencyPricingPlan, CompanyInquiry


@admin.register(AgencyPricingPlan)
class AgencyPricingPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "currency", 'period', "is_active", "order")
    list_editable = ("price", "is_active", "order")
    filter_horizontal = ("features",)


@admin.register(AgencyPlanFeature)
class AgencyPlanFeatureAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(CompanyInquiry)
class CompanyInquiryAdmin(admin.ModelAdmin):
    list_display = (
        "company_name",
        "name",
        "email",
        "phone",
        "created_at",
        "is_processed"
    )
    list_filter = ("is_processed", "created_at")
    list_editable = ("is_processed",)
    search_fields = ("company_name", "email")
