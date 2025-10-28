from django.db import models


class Platform(models.Model):
    HH = "HeadHunter"
    SUPER_JOB = "SuperJob"
    TELEGRAM = "Telegram"

    PLATFORM_NAME_CHOICES = [
        (HH, "HeadHunter"),
        (SUPER_JOB, "SuperJob"),
        (TELEGRAM, "Telegram"),
    ]

    name = models.CharField(choices=PLATFORM_NAME_CHOICES)

    def __str__(self):
        return f"{self.name}"


class Company(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.name}"


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Vacancy(models.Model):
    platform = models.ForeignKey(
        Platform, related_name="vacancies", on_delete=models.CASCADE, null=True
    )
    company = models.ForeignKey(
        Company, related_name="vacancies", on_delete=models.CASCADE, null=True
    )
    city = models.ForeignKey(
        City, related_name="vacancies", on_delete=models.SET_NULL, null=True
    )
    platform_vacancy_id = models.CharField(max_length=25, null=True)
    title = models.CharField(max_length=255)
    url = models.URLField(unique=True, default="", blank=True, null=True)
    salary = models.CharField(max_length=120, default="", blank=True, null=True)
    experience = models.CharField(max_length=50, default="", blank=True, null=True)
    employment = models.CharField(max_length=40, default="", blank=True, null=True)
    work_format = models.CharField(max_length=255, default="", blank=True, null=True)
    schedule = models.CharField(max_length=50, default="", blank=True, null=True)
    address = models.CharField(max_length=255, default="", blank=True, null=True)
    skills = models.TextField(default="", blank=True, null=True)
    description = models.TextField(default="", blank=True, null=True)
    education = models.CharField(max_length=30, default="", blank=True, null=True)
    contacts = models.CharField(max_length=250, default="", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField()

    def __str__(self):
        return f"{self.title} в {self.company}"
