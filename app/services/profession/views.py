from django.core.paginator import Paginator
from django.views import View
from inertia import render

from .models import Profession


class ProfessionView(View):

    def listing(self, request, *args, **kwargs):
        qs = Profession.objects.all()
        paginator = Paginator(qs, 25)
        page_number = request.GET.get("page")
        page = paginator.get_page(page_number)

        professions = [
            {
                "id": p.id,
                "name": p.name,
                "slug": p.slug,
            }
            for p in page.object_list
        ]

        props = {
            "professions": {
                "data": professions,
                "pagination": {
                    "page": page.number,
                    "pages": paginator.num_pages,
                    "has_next": page.has_next(),
                    "has_prev": page.has_previous(),
                    "next_page":
                        page.next_page_number() if page.has_next() else None,
                    "prev_page":
                        page.previous_page_number() if page.has_previous() else None,
                    "per_page": paginator.per_page,
                    "total": paginator.count,
                    },
                }
            }

        return render(request, "ProfessionPage/lists", props=props)
