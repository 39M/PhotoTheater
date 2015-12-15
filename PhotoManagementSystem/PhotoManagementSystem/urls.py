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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from PhotoManager import views
from PhotoManager.models import *

def showReq(request):
    ret = "<h1>GET</h1><br>"
    for i in request.GET:
        ret += i + " : " + request.GET[i] + "<br>"

    ret += "<h1>POST</h1><br>"
    for i in request.POST:
        ret += i + " : " + request.POST[i] + "<br>"

    return HttpResponse(ret)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', views.index),
    url(r'^home/$', login_required(views.Home.as_view())),
    url(r'^timeline/$', login_required(views.TimeLine.as_view())),
    url(r'^albumclass/$', login_required(views.AlbumClass.as_view())),
    url(r'^map/$', login_required(views.Map.as_view())),
    url(r'^photo/(?P<photo_id>[0-9]+)/$', login_required(views.PhotoView.as_view())),
    url(r'^filter/(?P<photo_id>[0-9]+)',login_required(views.Filter.as_view())),
    url(r'^photofilter/(?P<photo_id>[0-9]+)/(?P<filter_type>[a-z0-9]+)',login_required(views.PhotoFilter.as_view())),
    url(r'^signup/$', views.SignUp.as_view()),
    url(r'^signin/$', views.SignIn.as_view()),
    url(r'^signout/$', login_required(views.SignOut.as_view())),

    url(r'^uploadPhoto$', views.PhotoUpload.as_view()),
    url(r'^test/$', views.Test.as_view()),
    url(r'^test/album/', include(views.RestView(model=Album, field=["user", "name", "create_date", "update_date"]).urlGroup())),
    url(r'^test/photo/', include(views.RestView(model=Photo, field=["album", "name", "shot_date", "upload_date", "update_date", "latitude", "longitude", "location_text", "emotion", "origin_source", "source"]).urlGroup())),
    url(r'^test/showReq',showReq),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
