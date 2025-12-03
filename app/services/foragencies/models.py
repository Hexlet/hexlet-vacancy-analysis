
from django.db import models


class AgencyPricingPlan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.PositiveIntegerField(default=0)
    currency = models.CharField(max_length=3, default='₽')
    period = models.CharField(max_length=50, default='мес')
    description = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    features = models.ManyToManyField(
        'AgencyPlanFeature', related_name='plans', blank=True
    )

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class AgencyPlanFeature(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class CompanyInquiry(models.Model):
    company_name = models.CharField(max_length=200, blank=False)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f'Заявка от {self.company_name} ({self.email})'
