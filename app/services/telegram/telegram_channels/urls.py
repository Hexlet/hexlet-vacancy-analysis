from django.urls import path

from .views import AddChannelView, DeleteChannelView, IndexChannelView, ShowChannelView

urlpatterns = [
    path("", IndexChannelView.as_view(), name="channels_list"),
    path("add/", AddChannelView.as_view(), name="channels_add"),
    path("<int:pk>/show/", ShowChannelView.as_view(), name="channels_show"),
    path("<int:pk>/delete/", DeleteChannelView.as_view(), name="channels_delete"),
]
