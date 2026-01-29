from .base_parser import BaseVacancyParser


class HhVacancyParser(BaseVacancyParser):
    API_URL = 'https://api.hh.ru/vacancies'
    HEADERS = {"User-Agent": "HH-User-Agent"}

    def __init__(self):
        super().__init__()
        self.mapping = self.get_city_to_region_mapping(source='hh')

    def fetch_vacancies_list(self, search_params):
        data = self.fetch_items_list(search_params)
        return [item['id'] for item in data['items']]

    def parse_vacancies(self, search_params):
        vacancy_ids = self.fetch_vacancies_list(search_params)
        vacancies = []

        for vacancy_id in vacancy_ids:
            item = self.fetch_item_details(vacancy_id)
            vacancies.append(self.parse_vacancy(item))

        return vacancies

    def parse_vacancy(self, item):
        salary_data = item.get('salary', {})
        city = self.parse_nested_field(item, 'area')

        return {
            'hh_id': item.get('id'),
            'title': item.get('name', ''),
            'company_name': item.get('employer', {}).get('name', ''),
            'company_id': item.get('employer', {}).get('id', ''),
            'salary': self.format_salary(salary_data=salary_data),
            'published_at': item.get('published_at', ''),
            'url': item.get('alternate_url', ''),
            'experience': self.parse_nested_field(item, 'experience'),
            'employment': self.parse_nested_field(item, 'employment'),
            'schedule': self.parse_nested_field(item, 'schedule'),
            'work_format': self.parse_nested_field_list(item, 'work_format'),
            'work_schedule_by_days': self.parse_nested_field_list(
                item, 'work_schedule_by_days'),
            'working_hours': self.parse_nested_field_list(item, 'working_hours'),
            'key_skills': ', '.join([skill['name'] for skill in item.get(
                'key_skills', [])]),
            'description': self.parse_description(item.get('description')),
            'region': self.mapping.get(city, 'Unknown'),
            'city': city,
            'street': self.parse_nested_address(item, 'street'),
            'building': self.parse_nested_address(item, 'building'),
            'contacts': item.get('contacts', {}),
        }
