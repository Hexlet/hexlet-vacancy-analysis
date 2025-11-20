from django.db import models


class Profession(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class InertiaMeta:
        fields = ('name', 'slug', 'is_active')
