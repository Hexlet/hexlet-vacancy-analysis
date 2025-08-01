from django.db import models


class Vacancy(models.Model):
    hh_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True)
    company_name = models.CharField(max_length=255)
    company_id = models.IntegerField()
    area = models.CharField(max_length=100)
    salary = models.CharField(max_length=120, null=True)
    experience = models.CharField(max_length=50)
    employment = models.CharField(max_length=40, null=True)
    work_format = models.CharField(max_length=255, null=True)
    work_schedule_by_days = models.CharField(max_length=30, null=True)
    working_hours = models.CharField(max_length=20, null=True)
    schedule = models.CharField(max_length=50)
    key_skills = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100, null=True)
    street = models.CharField(max_length=100, null=True)
    building = models.CharField(max_length=15, null=True)
    contacts = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField()

    def __str__(self):
        return f'{self.title} в {self.company_name}'
