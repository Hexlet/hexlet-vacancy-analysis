from django.views import View
from inertia import render as inertia_render

from .models import PricingPlan


class PricingView(View):

    def get(self, request):
        plans = PricingPlan.objects.filter(is_active=True)
        props = {
            'plans': [
                {
                    'id': plan.id,
                    'name': plan.name,
                    'price': plan.price,
                    'currency': plan.currency,
                    'period': plan.period,
                    'description': plan.description,
                    'features': [
                        {'name': feature.name}
                        for feature in plan.features.all()
                    ]
                }
                for plan in plans
            ]
        }
        return inertia_render(request, 'PricingPage', props)