from django.urls import path

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
]
