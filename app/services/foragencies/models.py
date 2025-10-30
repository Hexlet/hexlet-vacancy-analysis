
from django.db import models


class AgencyPricingPlan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=3, default='RUB')
    period = models.CharField(max_length=50, default='месяц')
    description = models.TextField(blank=True)
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
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class CompanyInquiry(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f'Заявка от {self.name} ({self.email})'
