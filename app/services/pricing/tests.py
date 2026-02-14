from django.urls import reverse
from inertia.test import InertiaTestCase

from .models import PlanFeature, PricingPlan


class PricingTest(InertiaTestCase):
    def setUp(self):
        super().setUp()
        self.plan = PricingPlan.objects.create(name='Профи', price=490.00)
        self.feature = PlanFeature.objects.create(name='Безлимитный поиск')
        self.plan.features.add(self.feature)

    def test_pricing_view(self):
        self.client.get(reverse('pricing_page'))
        self.assertComponentUsed('PricingPage')
        props = self.props()
        self.assertIn('plans', props)
        self.assertEqual(len(props['plans']), 1)
        plan_props = props['plans'][0]
        self.assertEqual(plan_props['name'], 'Профи')
        self.assertEqual(len(plan_props['features']), 1)
        self.assertEqual(plan_props['features'][0]['name'], 'Безлимитный поиск')

    def test_pricing_view_no_active_plans(self):
        PricingPlan.objects.all().update(is_active=False)
        self.client.get(reverse('pricing_page'))
        self.assertComponentUsed('PricingPage')
        props = self.props()
        self.assertEqual(len(props['plans']), 0)

    def test_pricing_plan_creation_with_features(self):
        plan = PricingPlan.objects.create(name='Базовый', price=0.00, order=1)
        feature1 = PlanFeature.objects.create(name='Доступ к базовым функциям')
        feature2 = PlanFeature.objects.create(name='50 сохранений')
        plan.features.add(feature1, feature2)

        self.assertEqual(plan.features.count(), 2)
        self.assertIn(feature1, plan.features.all())
        self.assertEqual(str(plan), 'Базовый')

    def test_plan_feature_relations(self):
        feature = PlanFeature.objects.create(name='Безлимитный поиск_тест')
        plan1 = PricingPlan.objects.create(name='Профи_тест', price=490.00)
        plan2 = PricingPlan.objects.create(name='Премиум_тест', price=990.00)
        plan1.features.add(feature)
        plan2.features.add(feature)

        self.assertEqual(feature.plans.count(), 2)
        self.assertEqual(str(feature), 'Безлимитный поиск_тест')