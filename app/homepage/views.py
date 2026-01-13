from django.views import View
from inertia import render as inertia_render  # type: ignore

from .models import HomePageBlock


class HomePageView(View):
    def get(self, request):
        blocks = (
            HomePageBlock.objects.filter(is_active=True)
            .order_by("order")
            .values("id", "title", "block_type", "content", "order")
        )
        return inertia_render(request, "HomePage", props={"blocks": blocks})
