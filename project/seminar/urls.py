from django.urls import path
from . import views

urlpatterns = [
    # パラメータなし
    path('', views.index, name='index'),
]