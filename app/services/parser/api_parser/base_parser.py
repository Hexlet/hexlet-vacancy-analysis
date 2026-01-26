import logging
import os
import time

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from app.parser import get_fixture_data, save_data


class BaseVacancyParser:
    API_URL = None
    HEADERS = None
    DEFAULT_DELAY = 0.3
    CACHE_FILE = os.path.join(os.path.dirname(__file__), 'city_region_mapping.json')

    def __init__(self):
        self.session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        self.session.mount('https://', HTTPAdapter(max_retries=retries))

    def fetch_data(self, params=None, item_id=None):
        url = self.API_URL
        if item_id:
            url = f"{self.API_URL}/{item_id}"
            time.sleep(self.DEFAULT_DELAY)

        response = None
        try:
            response = self.session.get(
                url,
                params=params,
                headers=self.HEADERS,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.Timeout as e:
            logging.error(f"Timeout fetching data: {str(e)}")
            raise ValueError("Request timeout")
        except requests.RequestException as e:
            logging.error(f"Error fetching data: {str(e)}")
            status = response.status_code if response is not None else 'unknown'
            raise ValueError(f"Error fetching data: {status}")

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

    def get_city_to_region_mapping(self, source='hh'):
        if os.path.exists(self.CACHE_FILE):
            return get_fixture_data(self.CACHE_FILE)

        if source == 'hh':
            url = 'https://api.hh.ru/areas'
        elif source == 'superjob':
            url = 'https://api.superjob.ru/2.0/regions/combined/'
        else:
            raise ValueError('Unknown source')

        response = None
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
        except requests.Timeout as e:
            logging.error(f"Timeout fetching areas: {str(e)}")
            raise ValueError("Request timeout")
        except requests.RequestException as e:
            logging.error(f"Error fetching areas: {str(e)}")
            status = response.status_code if response is not None else 'unknown'
            raise ValueError(f"Error fetching areas: {status}")

        areas = response.json()
        mapping = {}

        if source == 'hh':
            mapping = self.parse_hh_areas(areas)

        elif source == 'superjob':
            mapping = self.parse_superjob_areas(areas)

        save_data(self.CACHE_FILE, mapping)
        return mapping

    def parse_hh_areas(self, areas):
        mapping = {}
        for country in areas:
            for region in country['areas']:
                region_name = region['name']
                for city in region['areas']:
                    mapping[city['name']] = region_name
                if not region['areas']:
                    mapping[region_name] = region_name
        return mapping

    def parse_superjob_areas(self, areas):
        mapping = {}
        for country in areas:
            for city in country['towns']:
                mapping[city['title']] = city['title']
            for region in country['regions']:
                region_name = region['title']
                for city in region['towns']:
                    mapping[city['title']] = region_name
                if not region['towns']:
                    mapping[region_name] = region_name
        return mapping