# coding: utf-8

# # api viewer
# from rest_framework import routers
# from .views import UserViewSet, TokenViewSet, ImageViewSet

# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'tokens', TokenViewSet)
# router.register(r'images', ImageViewSet)

from django.conf.urls import url
from api_v1 import views
urlpatterns = [
    url(r'^users/$', views.user_list),
    url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
]