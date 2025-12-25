import json

from django.core.exceptions import ValidationError
from django.http import HttpRequest, JsonResponse
from django.views import View
from inertia import InertiaResponse  # type: ignore
from inertia import render as inertia_render

from .models import AgencyPricingPlan, CompanyInquiry


class AgencyView(View):
    def get(self, request: HttpRequest) -> InertiaResponse:
        plans = AgencyPricingPlan.objects.filter(is_active=True, block_type="agencies")
        props = {
            "plans": [
                {
                    "id": plan.pk,
                    "title": plan.title,
                    "subtitle": plan.subtitle,
                    "price": plan.price,
                    "highlighted": plan.highlighted,
                    "features": [feature.name for feature in plan.features.all()],
                }
                for plan in plans
            ]
        }
        return inertia_render(
            request,
            "AgencyPricingPage",
            props,
        )

    def post(self, request: HttpRequest) -> JsonResponse:
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body.decode("utf-8"))
            except json.JSONDecodeError:
                return JsonResponse(
                    {"success": False, "error": "Invalid JSON format"}, status=400
                )
        else:
            data = request.POST.dict()

        try:
            inquiry = CompanyInquiry(
                company_name=data.get("company_name"),
                name=data.get("name"),
                email=data.get("email"),
                phone=data.get("phone"),
            )
            inquiry.full_clean()
            inquiry.save()
            return JsonResponse({"success": True}, status=201)
        except ValidationError as e:
            return JsonResponse({"success": False, "error": str(e)}, status=418)
        except Exception:
            return JsonResponse(
                {"success": False, "error": "Internal error"}, status=500
            )
