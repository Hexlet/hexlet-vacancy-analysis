from http import HTTPStatus

from django.urls import reverse
from inertia.test import InertiaTestCase

from app.services.parser.models import HhVacancy

from .models import Region


class RegionsTest(InertiaTestCase):
    def setUp(self):
        super().setUp()
        self.region = Region.objects.create(code='77', name='Москва')

    def test_region_model_creation(self):
        region = Region.objects.create(code='78', name='Санкт-Петербург')
        self.assertEqual(str(region), 'Санкт-Петербург (78)')
        self.assertEqual(Region.objects.count(), 2)

    def test_region_view_props(self):
        self.client.get(reverse('region_page', kwargs={'region_id': '77'}))
        self.assertComponentUsed('RegionPage')
        props = self.props()
        self.assertIn('region', props)
        self.assertIn('vacancies', props)
        self.assertEqual(props['region']['name'], 'Москва')
        self.assertEqual(props['region']['code'], '77')
        self.assertEqual(props['vacancies']['total_pages'], 1)

    def test_region_view_no_vacancies(self):
        Region.objects.create(code='99', name='Empty Region')
        self.client.get(reverse('region_page', kwargs={'region_id': '99'}))
        props = self.props()
        self.assertEqual(len(props['vacancies']['data']), 0)

    def test_region_view_invalid_id(self):
        response = self.client.get(reverse(
            'region_page',
            kwargs={'region_id': 'invalid'}
        ))
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)

    def test_region_view_paginator(self):
        for i in range(26):
            HhVacancy.objects.create(region='Москва', hh_id=i, company_id=i,
                                     title=f'Test {i}', company_name='Company',
                                     url=f'url{i}', salary='1000', city='Moscow',
                                     key_skills='skills', experience='exp',
                                     description='desc',
                                     published_at="2023-05-25T14:22:06+0300")
        self.client.get(reverse('region_page', kwargs={'region_id': '77'}) + '?page=2')
        props = self.props()
        self.assertEqual(props['vacancies']['current_page'], 2)
        self.assertTrue(props['vacancies']['has_previous'])
        self.assertFalse(props['vacancies']['has_next'])