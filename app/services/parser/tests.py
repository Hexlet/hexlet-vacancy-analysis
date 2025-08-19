from django.test import TestCase
from unittest.mock import patch, MagicMock
from .models import HhVacancy, SuperjobVacancy
from .api_parser.hh_parser import HhVacancyParser
from .api_parser.superjob_parser import SuperjobVacancyParser
from .api_parser.vacancy_saver import VacancySaver
from .views import base_vacancy_parser
from app.settings import FIXTURE_PATH
from app.parser import get_fixture_data
from http import HTTPStatus
import os

class VacancyTest(TestCase):
    fixtures = ['hh_vacancy_detail.json', 'sj_vacancy_detail.json']

    def setUp(self):
        data = get_fixture_data(os.path.join(FIXTURE_PATH, 'data_dump.json'))
        self.hh_data = data.get('hh_vacancy')
        self.sj_data = data.get('sj_vacancy')
        self.hh_list = data.get('hh_list_response')
        self.sj_list = data.get('sj_list_response')

        self.mock_request = MagicMock()
        self.mock_request.GET = {'query': 'Python'}

    @patch('app.services.parser.api_parser.base_parser.BaseVacancyParser.fetch_data')
    def test_hh_parser_fetch_vacancies(self, mock_fetch):
        mock_fetch.return_value = self.hh_list
        parser= HhVacancyParser()
        result = parser.fetch_vacancies_list({})

        self.assertEqual(result, ["12345678", "87654321"])

    @patch('app.services.parser.api_parser.base_parser.BaseVacancyParser.fetch_data')
    def test_hh_parser_parse_vacancy(self, mock_fetch):
        mock_fetch.return_value = self.hh_data
        parser = HhVacancyParser()
        result = parser.parse_vacancy(self.hh_data)

        self.assertEqual(result['id'], "120877600")
        self.assertEqual(result['name'], "Python Developer")
        self.assertEqual(result['salary'], "от 100000 до 200000 RUR")
        self.assertEqual(result['key_skills'], "Python, Django")

    @patch('app.services.parser.api_parser.base_parser.BaseVacancyParser.fetch_data')
    def test_sj_parser_parse_vacancies(self, mock_fetch):
        mock_fetch.return_value = self.sj_list
        parser = SuperjobVacancyParser()
        result = parser.parse_vacancies({})

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['id'], 987654)
        self.assertEqual(result[0]['name'], "Python разработчик")

    def test_vacancy_saver(self):
        saver = VacancySaver()
        test_data = {
            'hh_id': 999,
            'title': 'Test Vacancy',
            'company_name': 'Test Company',
            'url': 'http://test.com'
        }
        saver.save_vacancy(test_data, source='hh')
        self.assertTrue(HhVacancy.objects.filter(hh_id=999).exists())

    @patch('app.services.parser.views.HhVacancyParser')
    def test_base_vacancy_parser_success(self, mock_parser):
        mock_instance = mock_parser.return_value
        mock_instance.parse_vacancies.return_value = [{
            'hh_id': 111,
            'title': 'View Test',
            'company_name': 'Test Co',
            'url': 'http://test.com'
        }]

        response = base_vacancy_parser(
            self.mock_request,
            HhVacancyParser,
            HhVacancy,
            {}
        )

        self.assertEqual(response.status_code, HTTPStatus.OK.value)
        self.assertEqual(response.json()['saved_count'], 1)
