"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from app import views
from app.services.auth.password_reset.views import redirect_mail_link

urlpatterns = [
    path("", include("app.homepage.urls")),
    path("admin/", admin.site.urls),
    path("hh/", include("app.services.hh.hh_parser.urls")),
    path("superjob/", include("app.services.superjob.superjob_parser.urls")),
    path("telegram/", include("app.services.telegram.telegram_channels.urls")),
    path("auth/", include("app.services.auth.users.urls")),
    path("account/", include("app.services.account.urls")),
    path("ai-assistant/", include("app.services.ai.urls")),
    path("reset-password/", redirect_mail_link, name="password_reset_redirect"),
    path("pricing/", include("app.services.pricing.urls")),
    path("foragencies/", include("app.services.foragencies.urls")),
    path("parser/", include("app.services.parser.urls")),
    path("vacancies/", include("app.services.vacancies.urls")),
]

handler500 = views.custom_server_error
handler404 = views.custom_not_found_error
