from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .services.telegram.telegram_channels.models import Channel


class StaticSitemap(Sitemap):
    """
    Карта-сайта для статичных страниц
    """

    def items(self):
        return [
            # статические страницы
            "register_user",
            "channels_list",
        ]

    def location(self, item):
        return reverse(item)


class TelegramSitemap(Sitemap):
    """
    Карта-сайта для телеграм каналов
    """

    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return Channel.objects.all().order_by("username")

    def lastmod(self, obj):
        return obj.time_update
