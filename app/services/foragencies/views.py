import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View
from inertia import render as inertia_render

from .models import AgencyPricingPlan, CompanyInquiry


class AgencyView(View):
    def get(self, request):
        plans = AgencyPricingPlan.objects.filter(is_active=True)
        props = {
            "plans": [
                {
                    "id": plan.id,
                    "name": plan.name,
                    "price": f"{plan.price:,}",
                    "currency": plan.currency,
                    "period": plan.period,
                    "description": plan.description,
                    "features": [
                        {"name": feature.name} for feature in plan.features.all()
                    ],
                }
                for plan in plans
            ]
        }
        return inertia_render(request, "AgencyPricingPage", props)

    def post(self, request):
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body.decode("utf-8"))
            except json.JSONDecodeError:
                return JsonResponse(
                    {"success": False, "error": "Invalid JSON"}, status=400
                )
        else:
            data = request.POST.dict()

        if not all(key in data for key in ["company_name", "email"]):
            return JsonResponse(
                {
                    "success": False,
                    "error": "Обязательные поля: Название компании и email",
                },
                status=400,
            )
        if not data.get("email", "").count("@"):
            return JsonResponse(
                {"success": False, "error": "Некорректный email"}, status=400
            )
        try:
            CompanyInquiry.objects.create(
                company_name=data.get("company_name"),
                name=data.get("name"),
                email=data.get("email"),
                phone=data.get("phone", ""),
            )
            return JsonResponse({"success": True})

        except ValidationError as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
        except Exception:
            return JsonResponse(
                {"success": False, "error": "Internal error"}, status=500
            )
