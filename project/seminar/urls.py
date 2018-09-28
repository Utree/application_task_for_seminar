from django.urls import path
from . import views

urlpatterns = [
    # アップロード先のパス
    path('form', views.form, name='form'),
    # トップページ
    path('', views.index, name='index'),
]