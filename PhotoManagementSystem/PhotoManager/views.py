# coding=utf-8
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import auth
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context, RequestContext
from django.template.context_processors import csrf
from django.views.generic import *
from django.views.generic.edit import *
from PIL import Image, ExifTags
from PhotoManager.models import *
from config import *
from datetime import datetime
import os
import json
from pytz import timezone

TIME_ZONE = timezone('Asia/Shanghai')


class RestView(object):
    """ Restful API for Model CRUD operation """

    def __init__(self, model=None, field=None, success_url=None):
        self.model = model
        self.field = field
        self.success_url = success_url or '../..'

    def urlGroup(self):
        return [url(r'^$', self.asList().as_view()),
                url(r'^create/$', self.asCreate().as_view()),
                url(r'^update/(?P<pk>\d+)/$', self.asUpdate().as_view()),
                url(r'^delete/(?P<pk>\d+)/$', self.asDelete().as_view()),
                url(r'^deleteAll$', self.asDeleteAll().as_view()),
                url(r'^detail/(?P<pk>[-\w]+)/$', self.asDetail().as_view()),
                ]

    def asDeleteAll(self):
        t_model = self.model

        class DeleteAll(View):
            model = t_model

            def post(self, request, *args, **kwargs):
                deleteList = [int(key) for key in request.POST if request.POST[key] == u'on']
                self.model.objects.filter(pk__in=deleteList).delete()
                return redirect('./')

        return DeleteAll

    def asDetail(self):
        t_model = self.model

        class Detail(DetailView):
            model = t_model

        return Detail

    def asList(self):
        t_model = self.model

        class List(ListView):
            model = t_model

        return List

    def asCreate(self):
        t_model = self.model
        t_field = self.field
        t_success_url = self.success_url

        class Create(CreateView):
            model = t_model
            fields = t_field
            success_url = '../'
            template_name = 'base_test_form.html'

        return Create

    def asUpdate(self):
        t_model = self.model
        t_field = self.field
        t_success_url = self.success_url

        class Update(UpdateView):
            model = t_model
            fields = t_field
            success_url = t_success_url
            template_name_suffix = '_update_form'

        return Update

    def asDelete(self):
        t_model = self.model
        t_success_url = self.success_url

        class Delete(DeleteView):
            model = t_model
            success_url = t_success_url

        return Delete


def get_notice_info(data):
    if 'noticeType' in data and 'noticeTitle' in data and 'noticeText' in data:
        return {'noticeType': data['noticeType'],
                'noticeTitle': data['noticeTitle'],
                'noticeText': data['noticeText'], }
    else:
        return {}


class BaseView(View):
    """ Base view """

    def __init__(self, **kwargs):
        super(BaseView, self).__init__(**kwargs)
        self.context = {}

    def get(self, request):
        self.context = {}
        self.set_base(request)
        self.context.update(get_notice_info(request.GET))

    def set_gallery(self, request):
        photo_list = []
        for photo in Photo.objects.filter(album__user=request.user)[:5]:
            photo_list.append({
                'id': photo.id,
                'scr': photo.source.url,
                'location': photo.location_text,
                'description': photo.name,
            })

        self.context.update({
            'SlideShow': photo_list
        })

    def set_side_bar(self, request):
        self.set_gallery(request)

        # self.context.update({
        #     'runTime': {
        #         'ViewName': ''
        #     }
        # })

    def set_nav_bar(self, request):
        self.context.update({
            'user': {
                'name': request.user.username,
            }
        })

    def set_base(self, request):
        self.set_side_bar(request)
        self.set_nav_bar(request)

        self.context.update({
            'CONFIG': {
                'SITE': {
                    'TITLE': WEBSITE_TITLE
                },
            }
        })


# Redirect to home
def index(request):
    return redirect('/home/')


class Home(BaseView):
    """ Home view """

    def get(self, request):
        super(Home, self).get(request)

        # Send album list
        album_list = Album.objects.filter(user=request.user).order_by('name')
        self.context.update({
            'album_list': album_list
        })

        # Send photo list
        photo_list = Photo.objects.filter(album__user=request.user).order_by('-shot_date')
        self.context.update({
            'photo_list': photo_list
        })

        self.context = Context(self.context)
        self.context.update(csrf(request))
        print self.context
        return render(request, 'home.html', self.context)

    def post(self, request):
        data = request.POST
        print data
        user = request.user

        album = 0
        valid = True
        noticeText = ' '
        if data['photo_list'] == '[]':
            noticeText = u'未选择任何照片！'
            valid = False
        else:
            # New album or select album
            if 'newalbum' in data:
                if not data['newalbumname']:
                    noticeText = u'相册名不能为空！'
                    valid = False
                elif Album.objects.filter(name=data['newalbumname']):
                    noticeText = u'相册名已存在！'
                    valid = False
                else:
                    album = Album.objects.create(
                        user=user,
                        name=data['newalbumname'],
                    )
            else:
                print 'Album id = ' + data['albumname']
                album = Album.objects.get(id=data['albumname'])

        if not valid:
            noticeType = 'warn'
            noticeTitle = u'保存失败'
            return redirect('/home/?noticeType=%s&noticeTitle=%s&noticeText=%s' % (noticeType, noticeTitle, noticeText))

        # Create photos
        photo_list = json.loads(data['photo_list'])
        for name in photo_list:
            photo = Photo(
                album=album,
                name=name.split('.')[0],
            )

            if 'emotion' in data:
                photo.emotion = data['emotion']

            if 'comment' in data:
                photo.description = data['comment']

            # Save image source
            img = File(open('media/temp/' + name, 'rb'))
            img.name = name.replace('_' + name.split('_')[-1], '')
            photo.origin_source = img
            photo.source = img

            # PIL processing
            img = Image.open('media/temp/' + name)
            # Get shot date
            try:
                exif = {
                    ExifTags.TAGS[k]: v
                    for k, v in img._getexif().items()
                    if k in ExifTags.TAGS
                    }
                print exif
                shot_date = datetime.strptime(exif['DateTime'], '%Y:%m:%d %H:%M:%S')
            except:
                shot_date = datetime.strptime('1970:01:01', '%Y:%m:%d')

            photo.shot_date = TIME_ZONE.localize(shot_date)

            try:
                # Create thumb
                img.thumbnail((240, 100), Image.ANTIALIAS)
                img.save('media/temp/' + name + '.thumbnail', 'JPEG')
                # Save thumb
                img = File(open('media/temp/' + name + '.thumbnail', 'rb'))
                img.name = name.replace('_' + name.split('_')[-1], '')
                photo.thumb = img
            except:
                print 'Photo ' + name + ' created failed'
                valid = False
                noticeText = '部分格式错误的照片上传失败！'
                continue

            photo.save()

        if not valid:
            noticeType = 'warn'
            noticeTitle = u'警告'
            return redirect('/home/?noticeType=%s&noticeTitle=%s&noticeText=%s' % (noticeType, noticeTitle, noticeText))

        return redirect('/home/')


class PhotoUpload(View):
    """ Handle photo upload post """

    def get(self, request):
        return redirect('/home/')

    def post(self, request):
        # Save file with hash code for later verification
        hash_code = '_' + str(request.POST['hash'])
        data = request.FILES['file']
        default_storage.save('temp/' + data.name + hash_code, ContentFile(data.read()))

        return HttpResponse("OK")


class TimeLine(BaseView):
    """ Time line view """

    def get(self, request):
        super(TimeLine, self).get(request)

        # Send photo list data
        photo_list = Photo.objects.filter(album__user=request.user).order_by('-shot_date')
        self.context.update({
            'photo_list': photo_list
        })

        self.context = Context(self.context)
        self.context.update(csrf(request))
        print self.context
        return render(request, 'timelineSimple.html', self.context)


class Map(BaseView):
    """ Map view """

    def get(self, request):
        super(Map, self).get(request)

        # Send photo list data
        photo_list = Photo.objects.filter(album__user=request.user).order_by('-shot_date')
        self.context.update({
            'photo_list': photo_list
        })

        self.context = Context(self.context)
        self.context.update(csrf(request))
        print self.context
        return render(request, 'map.html', self.context)


class SignUp(View):
    """ Sign up view """

    def get(self, request):
        # Check if had signed in
        if request.user.is_authenticated():
            return redirect('/home/')

        context = Context({})
        context.update(csrf(request))
        return render(request, 'signup.html', context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        # Validate sign up
        if len(username) < 3:
            noticeText = u'用户名长度至少3位'
        elif User.objects.filter(username=username):
            noticeText = u'您选择的用户名已被使用'
        elif len(password) < 6:
            noticeText = u'密码长度至少6位'
        elif password != password_confirm:
            noticeText = u'两次密码输入不一致'
        else:
            user = User.objects.create_user(username=username, password=password)
            Album.objects.create(user=user, name='Default')
            noticeType = 'success'
            noticeTitle = u'注册成功'
            noticeText = ' '
            return redirect(
                '/signin/?noticeType=%s&noticeTitle=%s&noticeText=%s' % (noticeType, noticeTitle, noticeText))

        # Sign up fail, return warning info
        noticeType = 'warn'
        noticeTitle = u'注册失败'
        context = Context({
            'noticeType': noticeType,
            'noticeTitle': noticeTitle,
            'noticeText': noticeText,
            'username': username,
            'password': password,
            'password_confirm': password_confirm,
        })
        context.update(csrf(request))
        return render(request, 'signup.html', context)


class SignIn(View):
    """ Sign in view """

    def get(self, request):
        # Check if had signed in
        if request.user.is_authenticated():
            return redirect('/home/')

        # Check notice info
        context = get_notice_info(request.GET)

        context = Context(context)
        context.update(csrf(request))
        return render(request, 'login.html', context)

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        # Validate sign in
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                noticeType = 'success'
                noticeTitle = u'登录成功'
                noticeText = ' '

                redirect_url = '/home/'
                if 'next' in request.GET:
                    redirect_url = request.GET['next']

                return redirect(redirect_url + '?noticeType=%s&noticeTitle=%s&noticeText=%s' % (
                    noticeType, noticeTitle, noticeText))
            else:
                noticeText = u'账户被禁用'
        else:
            noticeText = u'用户名和密码不匹配'

        # Sign in fail
        noticeType = 'warn'
        noticeTitle = u'登录失败'
        context = Context({
            'noticeType': noticeType,
            'noticeTitle': noticeTitle,
            'noticeText': noticeText,
            'username': username,
            'password': password,
        })
        context.update(csrf(request))
        return render(request, 'login.html', context)


class SignOut(View):
    """ Sign out view """

    def get(self, request):
        auth.logout(request)
        noticeType = 'success'
        noticeTitle = u'已退出登录'
        noticeText = ' '
        return redirect(
            '/signin/?noticeType=%s&noticeTitle=%s&noticeText=%s' % (noticeType, noticeTitle, noticeText))


class Test(View):
    """ Test view for develop test """

    def get(self, request):
        context = Context(request.GET)
        context.update(csrf(request))
        return render(request, request.GET['v'] + '.html', context)
