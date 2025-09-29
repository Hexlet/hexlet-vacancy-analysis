from django.db import DataError, IntegrityError
from django.http import JsonResponse

from .api_parser.hh_parser import HhVacancyParser
from .api_parser.superjob_parser import SuperjobVacancyParser
from .api_parser.vacancy_saver import VacancySaver
from .models import HhVacancy, SuperjobVacancy


def base_vacancy_parser(request, parser_class, model, search_params):
    parser = parser_class()
    saver = VacancySaver()
    saved_count = 0
    errors = []

    vacancies = parser.parse_vacancies(search_params)
    for vacancy_data in vacancies:
        try:
            source = 'hh' if isinstance(parser, HhVacancyParser) else 'superjob'
            saver.save_vacancy(vacancy_data, source=source)
            saved_count += 1

        except IntegrityError:
            errors.append("Конфликт уникальности данных")
        except DataError as e:
            errors.append(f"Проблемы с типа данных {str(e)}")
        except (KeyError, ValueError) as e:
            errors.append(f"Проблема с данными: {str(e)}")
        except Exception as e:
            errors.append(f"Обнаружена непредвиденная ошибка  {str(e)}")
            continue

    return JsonResponse({
        'status': 'success',
        'saved_count': saved_count,
        'errors': errors,
        'message': f'Успешно сохранено {saved_count} вакансий'
    }, status=200)


def hh_vacancy_list(request):
    search_params = {
        'text': request.GET.get('query', 'Python'),
        'area': request.GET.get('area', 3),
        'per_page': request.GET.get('per_page', 4),
    }
    return base_vacancy_parser(request, HhVacancyParser, HhVacancy, search_params)


def superjob_vacancy_list(request):
    search_params = {
        'keyword': request.GET.get('query', 'Java'),
        'town': request.GET.get('town', 'Екатеринбург'),
        'count': request.GET.get('count', 4),
    }
    return base_vacancy_parser(
        request, SuperjobVacancyParser, SuperjobVacancy, search_params
    )
