"""PhotoManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from PhotoManager import views
from PhotoManager.models import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.Index.as_view()),
    url(r'^home/$', views.Home.as_view()),
    url(r'^signup/$', views.SignUp.as_view()),
    url(r'^signin/$', views.SignIn.as_view()),
    url(r'^signout/$', login_required(views.SignOut.as_view())),

    url(r'^test/$', views.Test.as_view()),
    url(r'^test/album/', include(views.RestView(model=Album, field=["user", "name", "create_date", "update_date"]).urlGroup())),
    url(r'^test/photo/', include(views.RestView(model=Photo, field=["album", "name", "shot_date", "upload_date", "update_date", "latitude", "longitude", "location_text", "emotion", "origin_source", "source"]).urlGroup())),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
