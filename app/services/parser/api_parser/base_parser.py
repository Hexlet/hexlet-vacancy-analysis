import time

import requests
from bs4 import BeautifulSoup


class BaseVacancyParser:
    API_URL = None
    HEADERS = None
    DEFAULT_DELAY = 0.3

    @classmethod
    def fetch_data(cls, params=None, item_id=None):
        url = cls.API_URL
        if item_id:
            url = f"{cls.API_URL}/{item_id}"
            time.sleep(cls.DEFAULT_DELAY)

        response = requests.get(url, params=params, headers=cls.HEADERS)
        response.raise_for_status()
        return response.json()

    @classmethod
    def fetch_items_list(cls, search_params):
        return cls.fetch_data(params=search_params)

    @classmethod
    def fetch_item_details(cls, item_id):
        return cls.fetch_data(item_id=item_id)

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
        field_data = data.get(field_name, {})
        if isinstance(field_data, dict):
            return field_data.get('name', '') or field_data.get('title', '')
        return str(field_data)
