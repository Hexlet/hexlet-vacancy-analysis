from django.shortcuts import get_object_or_404
# from inertia import render as inertia_render
from django.core.paginator import Paginator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

# from app.services.parser.models import HhVacancy, SuperjobVacancy
from .models import Region

class RegionView(View):
    pass
