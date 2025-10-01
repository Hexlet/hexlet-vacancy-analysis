from django.core.paginator import Paginator
from django.views import View
from inertia import render

from .models import Profession


class ProfessionView(View):

    def listing(self, request, *args, **kwargs):
        professions = Profession.objects.all()
        paginator = Paginator(professions, 25)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        vacancies = [
            {
                "id": v.id,
                "title": v.title,
                "company": v.company,
                "url": v.url,
            }
            for v in page_obj.object_list
        ]

        props = {
            "profession": {
                "id": professions.id,
                "name": professions.name,
                "slug": professions.slug
            },
            "vacancies": {
                "data": vacancies,
                }
            }

        return render(request, "ProfessionPage", props)
