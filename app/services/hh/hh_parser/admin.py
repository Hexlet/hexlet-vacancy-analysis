from django.contrib import admin

from .models import City, Company, Vacancy

admin.site.register(Vacancy)
admin.site.register(Company)
admin.site.register(City)

