# coding: utf-8

# api viewer
from rest_framework import routers
from .views import UserViewSet, TokenViewSet, ImageViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'token', TokenViewSet)
router.register(r'image', ImageViewSet)

from django.conf.urls import url
from api_v1 import views
urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^login/$', views.login),
    url(r'^images/$', views.images),
]