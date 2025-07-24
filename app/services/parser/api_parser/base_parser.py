import time

import requests
from bs4 import BeautifulSoup


class BaseVacancyParser:
    API_URL = None
    HEADERS = None
    DEFAULT_DELAY = 0.3

    def fetch_data(self, params=None, item_id=None):
        url = self.API_URL
        if item_id:
            url = f"{self.API_URL}/{item_id}"
            time.sleep(self.DEFAULT_DELAY)

        response = requests.get(url, params=params, headers=self.HEADERS)
        response.raise_for_status()
        return response.json()

    def fetch_items_list(self, search_params):
        return self.fetch_data(params=search_params)

    def fetch_item_details(self, item_id):
        return self.fetch_data(item_id=item_id)

    def parse_description(self, description):
        return BeautifulSoup(description or '', 'html.parser').get_text()

    def format_salary(self,
                      salary_data=None,
                      payment_from=None,
                      payment_to=None,
                      currency=None):
        if salary_data and isinstance(salary_data, dict):
            salary_from = salary_data.get('from')
            salary_to = salary_data.get('to')
            currency = salary_data.get('currency')
        else:
            salary_from = payment_from
            salary_to = payment_to

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

    def parse_nested_field(self, data, field_name):
        field_data = data.get(field_name, {})
        if isinstance(field_data, dict):
            return field_data.get('name', '') or field_data.get('title', '')
        return str(field_data)

    def parse_nested_field_list(self, data, field_name):
        field_data = data.get(field_name, [])
        if isinstance(field_data, list):
            return ''.join([item.get('name', '') for item in field_data])
        return field_data

    def parse_nested_address(self, data, field_name, field='address'):
        field_data = data.get(field, {})
        if isinstance(field_data, dict):
            return field_data.get(field_name, '')
        return str(field_data)
