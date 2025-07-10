from .base_parser import BaseVacancyParser


class HhVacancyParser(BaseVacancyParser):
    API_URL = 'https://api.hh.ru/vacancies'
    HEADERS = {"User-Agent": "HH-User-Agent"}

    @classmethod
    def fetch_vacancies_list(cls, search_params):
        """Получаем список ID вакансий"""
        data = cls.fetch_items_list(search_params)
        return [item['id'] for item in data['items']]

    @classmethod
    def parse_vacancies(cls, search_params):
        """Основной метод для получения и парсинга вакансий"""
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
        """Парсим конкретную вакансию"""
        address = item.get('address', {})
        salary_data = item.get('salary', {})

        return {
            'source_id': item.get('id'),
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
            'schedule': cls.parse_nested_field(item, 'schedule'),
            'work_schedule': item.get("work_schedule_by_days", [{}])[0].get("name", ""),
            'work_format': ', '.join(
                [work['name'] for work in item.get('work_format', [])]),
            'skills': ', '.join([skill['name'] for skill in item.get('key_skills', [])]),
            'description': cls.parse_description(item.get('description')),
            'city': address.get('city', ''),
            'street': address.get('street', ''),
            'building': address.get('building', ''),
            'employment': cls.parse_nested_field(item, 'employment'),
            'contacts': item.get('contacts', {}),
        }
