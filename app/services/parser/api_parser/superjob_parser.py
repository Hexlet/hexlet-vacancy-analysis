import os

from dotenv import load_dotenv

from .base_parser import BaseVacancyParser

load_dotenv()
SUPERJOB_API_KEY = os.getenv('SUPERJOB_API_KEY')


class SuperjobVacancyParser(BaseVacancyParser):
    API_URL = 'https://api.superjob.ru/2.0/vacancies'
    HEADERS = {"X-Api-App-Id": SUPERJOB_API_KEY}

    def __init__(self):
        super().__init__()
        self.mapping = self.get_city_to_region_mapping(source='superjob')

    def parse_vacancies(self, search_params):
        data = self.fetch_items_list(search_params)
        return [self.parse_vacancy(item) for item in data['objects']]

    def parse_vacancy(self, item):
        company = item.get('client', {})
        city = self.parse_nested_field(item, 'town')

        return {
            'superjob_id': item.get('id'),
            'title': item.get('profession', ''),
            'company_name': company.get('title', ''),
            'company_id': company.get('id', ''),
            'company_city': self.parse_nested_field(company, 'town'),
            'salary': self.format_salary(
                payment_from=item.get('payment_from'),
                payment_to=item.get('payment_to'),
                currency=item.get('currency')
            ),
            'published_at': item.get('date_published', ''),
            'url': item.get('link', ''),
            'experience': self.parse_nested_field(item, 'experience'),
            'type_of_work': self.parse_nested_field(item, 'type_of_work'),
            'place_of_work': self.parse_nested_field(item, 'place_of_work'),
            'education': self.parse_nested_field(item, 'education'),
            'description': self.parse_description(item.get('vacancyRichText')),
            'region': self.mapping.get(city, 'Unknown'),
            'city': city,
            'address': item.get('address', ''),
            'contacts': item.get('phone', ''),
        }
