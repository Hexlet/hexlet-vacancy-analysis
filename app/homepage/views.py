from django.views import View
from inertia import render as inertia_render  # type: ignore

from .models import HomePageBlock


class HomePageView(View):
    def get(self, request):
        blocks = HomePageBlock.objects.filter(is_active=True).order_by("order")
        blocks_data = []
        for block in blocks:
            blocks_data.append(
                {
                    "id": block.id,
                    "title": block.title,
                    "block_type": block.block_type,
                    "content": block.content,
                    "order": block.order,
                }
            )
        return inertia_render(request, "HomePage", props={"blocks": blocks_data})
