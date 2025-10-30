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
            'plans': [
                {
                    'id': plan.id,
                    'name': plan.name,
                    'price': float(plan.price),
                    'currency': plan.currency,
                    'period': plan.period,
                    'description': plan.description,
                    'features': [
                        {'name': feature.name, 'description': feature.description}
                        for feature in plan.features.all()
                    ]
                }
                for plan in plans
            ]
        }
        return inertia_render(request, 'AgencyPricingPage', props)

    def post(self, request):
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError:
                return JsonResponse(
                    {'success': False, 'error': 'Invalid JSON'},
                    status=400
                )
        else:
            data = request.POST.dict()

        if not all(key in data for key in ['name', 'email']):
            return JsonResponse(
                {'success': False, 'error': 'Обязательные поля: name и email'},
                status=400
            )
        if not data.get('email', '').count('@'):
            return JsonResponse(
                {'success': False, 'error': 'Некорректный email'},
                status=400
            )
        try:
            CompanyInquiry.objects.create(
                name=data.get('name'),
                email=data.get('email'),
                phone=data.get('phone', ''),
                message=data.get('message', ''),
            )
            return JsonResponse({'success': True, 'message': 'Заявка отправлена'})

        except ValidationError as e:
            return JsonResponse(
                {'success': False, 'error': str(e)},
                status=400
            )
        except Exception:
            return JsonResponse(
                {'success': False, 'error': 'Internal error'},
                status=500
            )