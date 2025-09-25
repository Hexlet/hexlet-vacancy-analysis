from django.urls import include, path

from . import views

urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register_user'),
    path(
        'activate/<uidb64>/<token>/',
        views.ActivateUser.as_view(),
        name='activate'
    ),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('csrf/', views.get_csrf_token, name='csrf'),
    path('draft/', views.draft_auth, name='auth_draft'),
    path('yandex/apply/', views.apply_yandex_profile, name='apply_yandex_profile'),
    path("github/", include("app.services.auth.github.urls")),
    path("yandex/", include("app.services.auth.yandex_id.urls")),
]
