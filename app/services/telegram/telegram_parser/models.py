from django.db import models


class KeyWord(models.Model):
    title = models.JSONField(verbose_name="title", default=list, blank=True)
    company = models.JSONField(verbose_name="company", default=list, blank=True)
    salary = models.JSONField(verbose_name="salary", default=list, blank=True)
    schedule = models.JSONField(verbose_name="schedule", default=list, blank=True)
    city = models.JSONField(verbose_name="city", default=list, blank=True)
    experience = models.JSONField(verbose_name="experience", default=list, blank=True)
    skills = models.JSONField(verbose_name="skills", default=list, blank=True)
    work_format = models.JSONField(verbose_name="work_format", default=list, blank=True)
    address = models.JSONField(verbose_name="address", default=list, blank=True)
    description = models.JSONField(verbose_name="description", default=list, blank=True)

    def __str__(self):
        return f"Telegram keywords - {self.id}"
