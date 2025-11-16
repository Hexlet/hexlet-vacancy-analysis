from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class BlogCategory(models.Model):
    name = models.CharField(
        max_length=100,
        null=False,
        unique=True,
        verbose_name=_("Name")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"))
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"))

    message_valid = _("Cannot delete category because it is in use.")

    class Meta:
        verbose_name = _("Blog Category")
        verbose_name_plural = _("Blog Categories")

    def __str__(self) -> str:
        return f"{self.name}"

    def can_delete(self):
        return not self.post_categories.exists()

    def delete(self, *args, **kwargs):
        if not self.can_delete():
            raise ValidationError(self.message_valid)
        super().delete(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Name"))
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at"))
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at"))
    message_valid = _("Tag is in use and cannot be deleted.")

    class Meta:
        verbose_name = _("Blog Tag")
        verbose_name_plural = _("Blog Tags")

    def __str__(self):
        return f"{self.name}"

    def can_delete(self):
        return not self.post_tags.exists()

    def delete(self, *args, **kwargs):
        if not self.can_delete():
            raise ValidationError(self.message_valid)
        super().delete(*args, **kwargs)


class BlogPost(models.Model):
    title = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=_("Title")
    )
    content_short = models.CharField(
        max_length=250,
        verbose_name=_("Short Content")
    )
    content_full = models.TextField(verbose_name=_("Full Content"))
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.PROTECT,
        related_name="post_categories",
        verbose_name=_("Blogs_categories")
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="post_tags",
        verbose_name=_("Tags"),
        blank=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_("Author")
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created at")
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated at")
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name=_("Published")
    )
    duration_minutes = models.PositiveIntegerField(
        verbose_name=_("Duration (minutes)"),
        help_text=_("Specify the number of minutes"),
        validators=[
            MinValueValidator(1),
            MaxValueValidator(60)
        ]
    )

    class Meta:
        verbose_name = _("Blog Post")
        verbose_name_plural = _("Blog Posts")

    def __str__(self):
        return f"{self.title}"
