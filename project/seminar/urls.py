from django.urls import path
from . import views

urlpatterns = [
    # トップページ
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('home', views.home, name='home'),
    path('add', views.add, name='add'),
    path('style_transfer', views.style_transfer, name="style_transfer"),
    path('manifest.json', views.manifest, name='manifest'),
]
