from django.db import models

class Region(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
