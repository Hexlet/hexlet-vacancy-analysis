from django.contrib import admin
from phonenumber_field.formfields import PhoneNumberField  # type: ignore
from phonenumber_field.widgets import PhoneNumberPrefixWidget  # type: ignore

from .models import AgencyPlanFeature, AgencyPricingPlan, CompanyInquiry


@admin.register(AgencyPricingPlan)
class AgencyPricingPlanAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "subtitle",
        "price",
        "is_active",
        "block_type",
        "highlighted",
        "features_list",
    )
    search_fields = ("title", "subtitle")
    list_filter = ("is_active", "block_type")
    list_editable = ("price", "is_active", "highlighted")
    filter_horizontal = ("features",)

    def features_list(self, obj):
        if obj.features.exists():
            return ", ".join([feature.name for feature in obj.features.all()])
        return "No features"


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
        "is_processed",
    )
    list_filter = ("is_processed", "created_at")
    list_editable = ("is_processed",)
    search_fields = ("company_name", "email")
    formfield_overrides = {
        PhoneNumberField: {"widget": PhoneNumberPrefixWidget},
    }
