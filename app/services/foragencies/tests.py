from http import HTTPStatus

from django.urls import reverse
from inertia.test import InertiaTestCase

from .models import AgencyPlanFeature, AgencyPricingPlan, CompanyInquiry


class ForAgenciesTest(InertiaTestCase):
    def setUp(self):
        super().setUp()
        self.plan = AgencyPricingPlan.objects.create(
            name='Стартовый_test',
            price=14990.00
        )
        self.feature = AgencyPlanFeature.objects.create(name='До 5 пользователей_test')
        self.plan.features.add(self.feature)

    def test_agency_view(self):
        self.client.get(reverse('foragencies_page'))
        self.assertComponentUsed('AgencyPricingPage')
        props = self.props()
        self.assertIn('plans', props)
        self.assertEqual(len(props['plans']), 1)
        plan_props = props['plans'][0]
        self.assertEqual(plan_props['name'], 'Стартовый_test')
        self.assertEqual(len(plan_props['features']), 1)
        self.assertEqual(plan_props['features'][0]['name'], 'До 5 пользователей_test')

    def test_agency_view_no_active_plans(self):
        AgencyPricingPlan.objects.all().update(is_active=False)
        self.client.get(reverse('foragencies_page'))
        self.assertComponentUsed('AgencyPricingPage')
        props = self.props()
        self.assertEqual(len(props['plans']), 0)

    def test_company_inquiry_creation(self):
        inquiry = CompanyInquiry.objects.create(
            name='Test Co',
            email='test@email.com',
            phone='123456',
            message='Inquiry'
        )
        self.assertEqual(inquiry.name, 'Test Co')
        self.assertFalse(inquiry.is_processed)
        self.assertEqual(str(inquiry), 'Заявка от Test Co (test@email.com)')

    def test_agency_view_post_inquiry(self):
        data = {
            'name': 'Post Co',
            'email': 'post@email.com',
            'phone': '789',
            'message': 'Post inquiry'
        }
        response = self.client.post(reverse('foragencies_page'), data)
        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        self.assertJSONEqual(
            response.content,
            {'success': True, 'message': 'Заявка отправлена'}
        )
        self.assertTrue(CompanyInquiry.objects.filter(name='Post Co').exists())

    def test_agency_view_post_error(self):
        data = {}
        response = self.client.post(reverse('foragencies_page'), data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST.value)
        self.assertJSONEqual(
            response.content,
            {'success': False, 'error': 'Обязательные поля: name и email', }
        )

    def test_agency_view_post_wrong_email(self):
        data = {
            'name': 'Post Co',
            'email': 'postemail.com',
            'phone': '789',
            'message': 'Post inquiry'
        }
        response = self.client.post(reverse('foragencies_page'), data)
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST.value)
        self.assertJSONEqual(
            response.content,
            {'success': False, 'error': 'Некорректный email', }
        )