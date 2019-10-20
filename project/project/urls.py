"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.urls import path
from django.conf.urls import include, url
# uploaded_files下を公開するための設定
from django.conf import settings
from django.conf.urls.static import static

# # api viewer(debug用)
from api_v1.urls import router as api_v1_router
from api_v1 import views

urlpatterns = [
    # ルートをseminarアプリに任せる
    url('^', include('seminar.urls')),

    # apiアプリ
    url(r'^v1/', include('api_v1.urls')),

    # api viewer(debug用)
    url(r'^v1/', include(api_v1_router.urls)),

    # 管理画面
    # path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # uploaded_file下を見えるようにする
