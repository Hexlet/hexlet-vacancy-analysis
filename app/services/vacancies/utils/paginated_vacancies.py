import asyncio
import logging

from asgiref.sync import sync_to_async
from django.core.paginator import Paginator
from django.db.models import Q

from app.services.hh.hh_parser.views import hh_vacancy_parse
from app.services.superjob.superjob_parser.views import superjob_vacancy_parse
from app.services.vacancies.models import Vacancy

VACANCIES_PER_PAGE = 5
PLATFORM_VACANCIES_QTY = VACANCIES_PER_PAGE * 2
HH_AREA_DEFAULT = 1
HH_VACANCY_CATEGORIES = [96, 165]
SUPERJOB_VACANCY_CATEGORY = 33

logger = logging.getLogger(__name__)


@sync_to_async
def get_search_vacancies(search_query: str = "") -> list[dict[str, str]]:
    qs = Vacancy.objects.select_related("company", "city", "platform")

    if search_query:
        terms = search_query.split()
        for term in terms:
            qs = qs.filter(
                Q(title__icontains=term)
                | Q(company__name__icontains=term)
                | Q(description__icontains=term)
                | Q(city__name__icontains=term)
            )

    return [
        {
            "id": v.platform_vacancy_id,
            "platform": v.platform.name if v.platform else "",
            "title": v.title,
            "salary": v.salary,
            "company": v.company.name if v.company else "",
            "city": v.city.name if v.city else "",
            "url": v.url,
            "skills": v.skills,
            "experience": v.experience,
            "employment": v.employment,
            "work_format": v.work_format,
            "schedule": v.schedule,
            "description": v.description,
            "address": v.address,
            "contacts": v.contacts,
            "published_at": v.published_at,
        }
        for v in qs
    ]


async def fetch_vacancies(search_query, page_obj):
    hh_params = {
        "text": search_query,
        "per_page": PLATFORM_VACANCIES_QTY,
        "page": page_obj.number - 1,
        "order_by": "publication_time",
        "professional_role": HH_VACANCY_CATEGORIES,
    }
    superjob_params = {
        "keyword": search_query,
        "count": PLATFORM_VACANCIES_QTY,
        "page": page_obj.number - 1,
        "catalogues": SUPERJOB_VACANCY_CATEGORY,
    }
    responses = await asyncio.gather(
        hh_vacancy_parse(params=hh_params),
        superjob_vacancy_parse(params=superjob_params),
    )
    return responses


def paginate(vacancies, page_number):
    paginator = Paginator(vacancies, VACANCIES_PER_PAGE)
    page_obj = paginator.get_page(page_number)

    return (vacancies, paginator, page_obj)


async def get_paginated_vacancies(request):
    page_number = int(request.GET.get("page", 1))
    search_query = request.GET.get("search", "").strip()
    vacancies = await get_search_vacancies(search_query)
    (vacancies, paginator, page_obj) = paginate(vacancies, page_number)

    if page_obj.number == paginator.num_pages:
        responses = await fetch_vacancies(search_query, page_obj)

        for response in responses:
            if response.status_code == 200:
                """Refetch paginated vacancies with new data"""
                vacancies = await get_search_vacancies(search_query)
                (_, paginator, page_obj) = paginate(vacancies, page_number)
            else:
                logger.error(f"Fetch error, status code: {response.status_code}")

    return {
        "pagination": {
            "current_page": page_obj.number,
            "total_pages": paginator.num_pages,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
            "next_page_number": page_obj.next_page_number()
            if page_obj.has_next()
            else None,
            "previous_page_number": page_obj.previous_page_number()
            if page_obj.has_previous()
            else None,
        },
        "vacancies": page_obj.object_list,
    }
