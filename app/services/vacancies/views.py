from django.views import View
from inertia import render as inertia_render

from .utils.paginated_vacancies import get_paginated_vacancies


class VacancyListView(View):
    async def get(self, request):
        pagination_vacancies = await get_paginated_vacancies(request)
        return inertia_render(
            request,
            "VacanciesPage",
            props={
                "vacancies": pagination_vacancies["vacancies"],
                "pagination": pagination_vacancies["pagination"],
            },
        )
