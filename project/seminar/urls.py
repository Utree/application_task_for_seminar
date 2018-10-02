from django.urls import path
from . import views

urlpatterns = [
    # トップページ
    path('', views.index, name='index'),
]