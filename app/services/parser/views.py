from django.http import JsonResponse

from .models import SuperJob, Vacancy
from .services import HhVacancyParser, SuperjobVacancyParser, VacancySaver


def base_vacancy_parser(request, parser_class, model, search_params):
    model.objects.all().delete()

    try:
        vacancies = parser_class.parse_vacancies(search_params)

        saved_count = 0
        errors = []

        for vacancy_data in vacancies:
            try:
                source = 'hh' if parser_class == HhVacancyParser else 'superjob'
                VacancySaver.save_vacancy(vacancy_data, source=source)
                saved_count += 1
            except Exception as e:
                errors.append(f"Ошибка при сохранении: {str(e)}")
                continue

        return JsonResponse({
            'status': 'success',
            'saved_count': saved_count,
            'errors': errors,
            'message': f'Успешно сохранено {saved_count} вакансий'
        }, status=200)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Ошибка при парсинге: {str(e)}'
        }, status=500)


def hh_vacancy_list(request):
    """Обработчик для вакансий с HH"""
    search_params = {
        'text': request.GET.get('query', 'Python'),
        'area': request.GET.get('area', 1),
        'per_page': request.GET.get('per_page', 4),
    }
    return base_vacancy_parser(request, HhVacancyParser, Vacancy, search_params)


def superjob_vacancy_list(request):
    """Обработчик для вакансий с SuperJob"""
    search_params = {
        'keyword': request.GET.get('query', 'Python'),
        'town': request.GET.get('town', 'Москва'),
        'count': request.GET.get('count', 4),
    }
    return base_vacancy_parser(request, SuperjobVacancyParser, SuperJob, search_params)
