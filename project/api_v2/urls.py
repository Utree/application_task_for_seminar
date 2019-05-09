# coding: utf-8
from django.conf.urls import url
from api_v2 import views
urlpatterns = [
    url(r'^images/$', views.images),
]
