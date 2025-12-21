from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class AgencyPricingPlan(models.Model):
    BLOCK_TYPE = (
        ("agencies", "Агентсва"),
        ("tariffs", "Тарифы"),
    )
    title = models.CharField(max_length=100, verbose_name="Заголовок")
    subtitle = models.CharField(max_length=50, verbose_name="Подзаголовок")
    price = models.CharField(
        max_length=100, verbose_name="Цена", help_text="₽10,000 /мес"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    block_type = models.CharField(
        max_length=20,
        choices=BLOCK_TYPE,
        verbose_name="Тип блока",
    )
    highlighted = models.BooleanField(default=False, verbose_name="Выдиление")

    features = models.ManyToManyField(
        "AgencyPlanFeature",
        related_name="plans",
        blank=True,
        verbose_name="Характеристики",
    )

    class Meta:
        verbose_name = "Блок тарифов и агенств"
        verbose_name_plural = "Блоки тарифов и агенств"

    def __str__(self):
        return self.title


class AgencyPlanFeature(models.Model):
    name = models.CharField(max_length=200, verbose_name="Характеристика")

    class Meta:
        verbose_name = "Характеристика"
        verbose_name_plural = "Характеристики"

    def __str__(self):
        return self.name


class CompanyInquiry(models.Model):
    company_name = models.CharField(max_length=200, verbose_name="Компания")
    name = models.CharField(max_length=200, verbose_name="Имя")
    email = models.EmailField(verbose_name="Почта")
    phone = PhoneNumberField(verbose_name="Телефон", region="RU")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_processed = models.BooleanField(default=False, verbose_name="Обработан")

    class Meta:
        verbose_name = "Заявка от компании"
        verbose_name_plural = "Заявки от компаний"

    def __str__(self):
        return f"Заявка от {self.company_name} ({self.email})"
