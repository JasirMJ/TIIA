"""Tiia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path

#
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include



# from Project import views
from Project import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url('detect/',views.DetectView.as_view()),
    url('getAds/',views.AdverticementView.as_view()),
    url('announce/',views.Announce.as_view()),
    url('speak/',views.SpeakMessage.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)