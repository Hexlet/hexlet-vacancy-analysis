import os

from .base_parser import BaseVacancyParser
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')


class SuperJobVacancyParser(BaseVacancyParser):
    API_URL = 'https://api.superjob.ru/2.0/vacancies'
    HEADERS = {"X-Api-App-Id": SECRET_KEY}

    @classmethod
    def parse_vacancy(cls, item):
        company = item.get('client', {})

        return {
            'source_id': item.get('id'),
            'title': item.get('profession', ''),
            'company_name': company.get('title', ''),
            'company_id': company.get('id', ''),
            'company_city': cls.parse_nested_field(company, 'town'),
            'salary': cls.format_salary(
                item.get('payment_from'),
                item.get('payment_to'),
                item.get('currency')
            ),
            'published_at': item.get('date_published', ''),
            'url': item.get('link', ''),
            'experience': cls.parse_nested_field(item, 'experience'),
            'type_of_work': cls.parse_nested_field(item, 'type_of_work'),
            'place_of_work': cls.parse_nested_field(item, 'place_of_work'),
            'educatiohn': cls.parse_nested_field(item, 'education'),
            'description': cls.parse_description(item.get('vacancyRichText')),
            'city': cls.parse_nested_field(item, 'city'),
            'address': item.get('address', ''),
            'contacts': item.get('phone', ''),
        }
