from .base_parser import BaseVacancyParser


class HhVacancyParser(BaseVacancyParser):
    API_URL = 'https://api.hh.ru/vacancies'
    HEADERS = {"User-Agent": "HH-User-Agent"}

    @classmethod
    def fetch_vacancies_list(cls, search_params):
        data = cls.fetch_items_list(search_params)
        return [item['id'] for item in data['items']]

    @classmethod
    def parse_vacancies(cls, search_params):
        vacancy_ids = cls.fetch_vacancies_list(search_params)
        vacancies = []

        for vacancy_id in vacancy_ids:
            try:
                item = cls.fetch_item_details(vacancy_id)
                vacancies.append(cls.parse_vacancy(item))
            except Exception as e:
                print(f"Ошибка при обработке вакансии {vacancy_id}: {str(e)}")
                continue

        return vacancies

    @classmethod
    def parse_vacancy(cls, item):
        address = item.get('address', {})
        salary_data = item.get('salary', {})

        return {
            'hh_id': item.get('id'),
            'title': item.get('name', ''),
            'company_name': item.get('employer', {}).get('name', ''),
            'company_id': item.get('employer', {}).get('id', ''),
            'area': cls.parse_nested_field(item, 'area'),
            'salary': cls.format_salary(
                salary_data.get('from'),
                salary_data.get('to'),
                salary_data.get('currency')
            ),
            'published_at': item.get('published_at', ''),
            'url': item.get('alternate_url', ''),
            'experience': cls.parse_nested_field(item, 'experience'),
            'employment': cls.parse_nested_field(item, 'employment'),
            'schedule': cls.parse_nested_field(item, 'schedule'),
            'work_format': cls.parse_nested_field(item, 'work_format'),
            'work_schedule_by_days': cls.parse_nested_field(
                item, 'work_schedule_by_days'),
            'working_hours': cls.parse_nested_field(item, 'working_hours'),
            'key_skills': ', '.join([skill['name'] for skill in item.get(
                'key_skills', [])]),
            'description': cls.parse_description(item.get('description')),
            'city': address.get('city', ''),
            'street': address.get('street', ''),
            'building': address.get('building', ''),
            'contacts': item.get('contacts', {}),
        }
