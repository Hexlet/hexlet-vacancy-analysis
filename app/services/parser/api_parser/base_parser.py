import requests
from bs4 import BeautifulSoup


class BaseVacancyParser:
    API_URL = None
    HEADERS = None

    @classmethod
    def fetch_vacancies(cls, search_params):
        response = requests.get(cls.API_URL, params=search_params, headers=cls.HEADERS)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def parse_description(description):
        return BeautifulSoup(description or '', 'html.parser').get_text()

    @staticmethod
    def format_salary(salary_from, salary_to, currency):
        if not salary_from and not salary_to:
            return 'По договоренности'

        parts = []
        if salary_from:
            parts.append(f"от {salary_from}")
        if salary_to:
            parts.append(f"до {salary_to}")
        if currency:
            parts.append(currency)
        return ' '.join(parts)

    @staticmethod
    def parse_nested_field(data, field_name):
        return data.get(field_name, {}).get('name', '') or data.get(field_name, {}).get('title', '')

    @classmethod
    def parse_vacancy(cls, item):
        raise NotImplementedError("Subclasses must implement this method")
