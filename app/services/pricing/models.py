from django.db import models


class PricingPlan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='RUB')
    period = models.CharField(max_length=50, default='месяц')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    features = models.ManyToManyField('PlanFeature', related_name='plans', blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class PlanFeature(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

