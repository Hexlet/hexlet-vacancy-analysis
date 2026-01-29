from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.views import View
from inertia import render as inertia_render

from app.services.parser.models import HhVacancy, SuperjobVacancy

from .models import Region


class RegionView(View):

    def get(self, request, region_id):
        region = get_object_or_404(Region, code=region_id)

        hh_vacancies = HhVacancy.objects.filter(region=region.name)
        sj_vacancies = SuperjobVacancy.objects.filter(region=region.name)
        all_vacancies = list(hh_vacancies) + list(sj_vacancies)

        paginator = Paginator(all_vacancies, 25)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        vacancies_data = [
            {
                "id": vacancy.id if hasattr(vacancy, 'id')
                        else vacancy.hh_id or vacancy.superjob_id,
                "title": vacancy.title,
                "company": vacancy.company_name,
                "url": vacancy.url,
                "description": vacancy.description,
                "salary": vacancy.salary,
                "city": vacancy.city,
                "key_skills": vacancy.key_skills,
                "experience": vacancy.experience,
            }
            for vacancy in page_obj.object_list
        ]

        props = {
            "region": {
                "id": region.id,
                "name": region.name,
                "code": region.code
            },
            "vacancies": {
                "data": vacancies_data,
                "current_page": page_obj.number,
                "total_pages": paginator.num_pages,
                "has_next": page_obj.has_next(),
                "has_previous": page_obj.has_previous(),
            }
        }

        return inertia_render(request, "RegionPage", props)