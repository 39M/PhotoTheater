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
from PIL import Image, ImageFilter, ExifTags
from PhotoManager.models import *
from config import *
from datetime import datetime
from pytz import timezone
from Library import filter_lib
import os
import json

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
                'noticeText': data['noticeText'],}
    else:
        return {}


def get_page_info(viewName):
    title = {
        'home': u'照片上传',
        'timeline': u'时间轴',
        'map': u'照片地图',
        'album': u'相册',
    }
    context = {
        'view': viewName,
        'title': title[viewName],
    }
    return context


class BaseView(View):
    """ Base view """

    def __init__(self, **kwargs):
        super(BaseView, self).__init__(**kwargs)
        self.context = {}
        self.simple_view = False

    def get(self, request):
        self.context = {}
        self.set_base(request)
        self.context.update(get_notice_info(request.GET))

    def set_gallery(self, request):
        photo_list = []
        for photo in Photo.objects.filter(album__user=request.user).order_by('upload_date')[:10]:
            photo_list.append({
                'id': photo.id,
                'scr': photo.thumb.url,
                'location': photo.location_text,
                'description': photo.description,
            })

        self.context.update({
            'SlideShow': photo_list
        })

    def set_nav_bar(self, request):
        self.context.update({
            'user': {
                'name': request.user.username,
            }
        })

    def set_base(self, request):
        self.context.update({
            'CONFIG': {
                'SITE': {
                    'TITLE': WEBSITE_TITLE
                },
            },
        })

        if self.simple_view:
            return

        self.set_gallery(request)
        self.set_nav_bar(request)

        self.context.update({
            'photo_number': Photo.objects.filter(album__user=request.user).count(),
            'photo_number_this_month': Photo.objects.filter(album__user=request.user,
                                                            upload_date__month=datetime.now().month).count(),
        })


# Redirect to home
def index(request):
    return redirect('/home/')


class Home(BaseView):
    """ Home view """

    def get(self, request):
        super(Home, self).get(request)
        self.context.update(get_page_info('home'))

        # Send album and photo list
        self.context.update({
            'album_list': Album.objects.filter(user=request.user).order_by('name'),
            'photo_list': Photo.objects.filter(album__user=request.user).order_by('-upload_date')
        })

        self.context = Context(self.context)
        self.context.update(csrf(request))
        print self.context
        return render(request, 'home.html', self.context)

    def post(self, request):
        data = request.POST
        user = request.user
        print data

        # Init variables
        album = 0
        valid = True
        noticeText = ''
        noticeTitle = ''

        # Validate
        if data['photo_list'] == '[]':
            noticeText = u'未选择任何照片！'
            valid = False
        elif 'newalbum' in data:
            if not data['newalbumname']:
                noticeText = u'相册名不能为空！'
                valid = False
            elif Album.objects.filter(user=request.user, name=data['newalbumname']):
                noticeText = u'相册名已存在！'
                valid = False
            else:
                # Create new album
                album = Album.objects.create(
                        user=user,
                        name=data['newalbumname'],
                )
        else:
            # Select album
            album = Album.objects.filter(user=request.user, id=data['albumname'])
            if album:
                album = album[0]
            else:
                noticeText = u'未知错误：相册id：' + data['albumname']
                print 'Error album id = ' + data['albumname']
                valid = False

        if not valid:
            # Not valid with form
            noticeTitle = u'保存失败'
        else:
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
                hash_code = '_' + name.split('_')[-1] + '.'
                file_name = hash_code.join(name[:name.rfind('_')].split('.'))
                img.name = file_name
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
                    shot_date = datetime.strptime(exif['DateTime'], '%Y:%m:%d %H:%M:%S')
                except:
                    shot_date = datetime.strptime('1970:01:01', '%Y:%m:%d')

                photo.shot_date = TIME_ZONE.localize(shot_date)

                try:
                    # Create thumb
                    img.thumbnail((480, 200), Image.ANTIALIAS)
                    img.save('media/temp/' + name + '.thumbnail', 'JPEG')
                    # Save thumb
                    img = File(open('media/temp/' + name + '.thumbnail', 'rb'))
                    img.name = file_name
                    photo.thumb = img
                    photo.origin_thumb = img
                except:
                    # Create thumb failed
                    print 'Photo ' + name + ' created failed'
                    valid = False
                    noticeText = u'部分格式错误的照片上传失败！'
                    continue

                photo.save()

            if not valid:
                # Upload error
                noticeTitle = u'警告'

        if not valid:
            # Upload fail
            noticeType = 'warn'
        else:
            # Upload success
            noticeType = 'success'
            noticeTitle = u'上传成功！'
            noticeText = ' '

        return HttpResponse(json.dumps({
            'noticeType': noticeType,
            'noticeTitle': noticeTitle,
            'noticeText': noticeText,
        }))


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
        self.context.update(get_page_info('timeline'))

        # Send photo list data
        self.context.update({
            'photo_list': Photo.objects.filter(album__user=request.user).order_by('-shot_date')
        })

        self.context = Context(self.context)
        self.context.update(csrf(request))
        print self.context
        return render(request, 'timelineSimple.html', self.context)


class AlbumClass(BaseView):
    """ Time line view """

    def get(self, request):
        super(AlbumClass, self).get(request)
        self.context.update(get_page_info('album'))

        # Send photo list data
        self.context.update({
            'photo_list': Photo.objects.filter(album__user=request.user).order_by('-album_id', 'update_date')
        })

        self.context = Context(self.context)
        self.context.update(csrf(request))
        print self.context
        return render(request, 'albumClass.html', self.context)


class Map(BaseView):
    """ Map view """

    def get(self, request):
        super(Map, self).get(request)
        self.context.update(get_page_info('map'))

        # Send photo list data
        self.context.update({
            'photo_list': Photo.objects.filter(album__user=request.user).order_by('-shot_date')
        })

        self.context = Context(self.context)
        self.context.update(csrf(request))
        print self.context
        return render(request, 'map.html', self.context)


class PhotoView(BaseView):
    """ Single photo display view """

    def __init__(self, **kwargs):
        super(PhotoView, self).__init__(**kwargs)
        self.simple_view = True

    def get(self, request, photo_id=0):
        super(PhotoView, self).get(request)

        # Check if photo with the id exist
        photo = Photo.objects.filter(album__user=request.user, id=photo_id)
        if not photo:
            return redirect('/home/')
        else:
            photo = photo[0]

        self.context.update({
            'album_list': Album.objects.filter(user=request.user).order_by('name'),
            'photo': photo,
        })

        self.context = Context(self.context)
        self.context.update(csrf(request))
        return render(request, 'photo.html', self.context)

    def post(self, request, photo_id):
        data = request.POST
        user = request.user
        noticeText = u''
        print request.POST

        photo = Photo.objects.filter(album__user=user, id=data['id'])
        for i in [1]:
            if not photo:
                noticeText = u'照片不存在！'
                break
            else:
                photo = photo[0]
                if not data['name']:
                    noticeText = u'照片名不能为空！'
                    break

                if 'newalbum' in data:
                    if not data['newalbumname']:
                        noticeText = u'相册名不能为空！'
                        break
                    elif Album.objects.filter(user=user, name=data['newalbumname']):
                        noticeText = u'相册名已存在！'
                        break
                    else:
                        # Create new album
                        album = Album.objects.create(
                                user=user,
                                name=data['newalbumname'],
                        )
                else:
                    # Select album
                    print 'Album id = ' + data['albumname']
                    album = Album.objects.filter(user=user, id=data['albumname'])
                    if album:
                        album = album[0]
                    else:
                        noticeText = u'未知错误：相册id：' + data['albumname']
                        break

                photo.name = data['name']
                photo.album = album
                photo.latitude = data['lat']
                photo.longitude = data['lng']
                print data['shot_date']
                print type(data['shot_date'])
                # photo.shot_date = data['shot_date']
                if 'emotion' in data:
                    photo.emotion = data['emotion']
                photo.description = data['description']

                '''Save filter start'''
                if 'filter' in data:
                    # if True:
                    filter_type = data['filter']
                    # filter_type = 'origin'
                    if filter_type == 'origin':
                        photo.source.delete()
                        target = File(open(photo.origin_source.path, 'rb'))
                        photo.source = target

                        photo.thumb.delete()
                        target = File(open(photo.origin_thumb.path, 'rb'))
                        photo.thumb = target
                    elif filter_type in FILTER_TYPE:
                        pure_name = photo.source.name
                        pure_name = pure_name[pure_name.rfind('/') + 1:]
                        filter_path = photo.source.path
                        filter_path = filter_path[:filter_path.rfind('.')]
                        target_name = ('_' + filter_type + '.').join(pure_name.split('.'))
                        target_path = os.path.join(filter_path, target_name)
                        if os.path.exists(target_path):
                            target = File(open(target_path, 'rb'))
                            photo.source.delete()
                            photo.source = target
                            photo.source.name = pure_name
                        else:
                            noticeText = u'滤镜尚未处理完毕!'
                            print 'Not done yet filter type: ' + filter_type
                            break

                        target_thumb = os.path.join(filter_path, Filter.thumb_name(pure_name, filter_type))
                        target = File(open(target_thumb, 'rb'))
                        photo.thumb.delete()
                        photo.thumb = target
                        photo.thumb.name = pure_name
                    else:
                        noticeText = u'所选滤镜不合法！'
                        print 'Error filter type: ' + filter_type
                        break
                '''Save filter end'''

                photo.save()

        if noticeText:
            noticeType = 'warn'
            noticeTitle = u'保存失败'
        else:
            noticeType = 'success'
            noticeTitle = u'保存成功'
            noticeText = ' '

        return HttpResponse(json.dumps(({
            'noticeType': noticeType,
            'noticeTitle': noticeTitle,
            'noticeText': noticeText,
        })))


FILTER_TYPE = ['filter1977', 'blackwhite', 'blackwhite2', 'gauss', 'glow',
               'oldmovie', 'oldphoto', 'processing', 'spherize', 'sundancekid', ]


# 'beeps', 'baozou', 'enlarge']


class PhotoDeleteView(BaseView):
    def __init__(self, **kwargs):
        super(PhotoDeleteView, self).__init__(**kwargs)
        self.simple_view = True

    def get(self, request, photo_id=0):
        photo = Photo.objects.filter(album__user=request.user, id=photo_id)
        if not photo:
            print 'No photo with id ' + str(photo_id)
            return HttpResponse('Fail')
        photo[0].delete()
        return HttpResponse('OK')


class PhotoFilter(BaseView):
    def __init__(self, **kwargs):
        super(PhotoFilter, self).__init__(**kwargs)
        self.simple_view = True

    def get(self, request, photo_id=0, filter_type=""):
        print request
        photo = Photo.objects.filter(album__user=request.user, id=photo_id)
        if not photo:
            print 'No photo with id ' + str(photo_id)
            return HttpResponseRedirect('/static/images/grass-blades.jpg')
        else:
            photo = photo[0]

        if filter_type == 'origin':
            return HttpResponseRedirect(photo.origin_source.url)

        if filter_type not in FILTER_TYPE:
            print 'No filter with type' + filter_type
            return HttpResponseRedirect('/static/images/grass-blades.jpg')

        pure_name = photo.source.name
        pure_name = pure_name[pure_name.rfind('/') + 1:]
        filter_path = photo.source.path
        filter_path = filter_path[:filter_path.rfind('.')]
        target_name = ('_' + filter_type + '.').join(pure_name.split('.'))
        target_path = os.path.join(filter_path, target_name)
        image_url = photo.source.name
        image_url = image_url[:image_url.rfind('.')]
        image_url = '/media/' + image_url + '/'
        if not os.path.exists(target_path):
            try:
                eval('filter_lib.' + filter_type)(photo.origin_source.path, target_path)
            except:
                print 'Create' + filter_type + 'filter Error'

        return HttpResponseRedirect(image_url + target_name)


class Filter(View):
    def __init__(self, **kwargs):
        super(Filter, self).__init__(**kwargs)
        self.context = {}

    @staticmethod
    def thumb_name(pure_name, filter_name):
        return ('_' + filter_name + '_thumb.').join(pure_name.split('.'))

    def get(self, request, photo_id=0):
        self.context = {}

        # Check if photo with the id exist
        photo = Photo.objects.filter(album__user=request.user, id=photo_id)
        if not photo:
            return redirect('/home/')
        else:
            photo = photo[0]

        pure_name = photo.source.name
        pure_name = pure_name[pure_name.rfind('/') + 1:]
        filter_path = photo.source.path
        filter_path = filter_path[:filter_path.rfind('.')]

        # Generate filter thumbs
        if not os.path.isdir(filter_path):
            os.makedirs(filter_path)
        thumb_path = photo.thumb.path
        for filter_name in FILTER_TYPE:
            target_name = os.path.join(filter_path, self.thumb_name(pure_name, filter_name))
            if not os.path.exists(target_name):
                try:
                    eval('filter_lib.' + filter_name)(thumb_path, target_name)
                except:
                    print 'Create' + filter_name + 'thumb Error'

        thumb_url = photo.source.name
        thumb_url = thumb_url[:thumb_url.rfind('.')]
        thumb_url = '/media/' + thumb_url + '/'
        filters = [{
            'name': 'origin',
            'example': photo.origin_thumb.url,
        }]
        for filter_name in FILTER_TYPE:
            filters.append({
                'name': filter_name,
                'example': thumb_url + self.thumb_name(pure_name, filter_name),
            })
        print filters

        self.context.update({
            'filters': filters,
            'id': photo_id,
        })

        self.context = Context(self.context)
        self.context.update(csrf(request))
        return render(request, 'filter.html', self.context)


class SignUp(BaseView):
    """ Sign up view """

    def __init__(self, **kwargs):
        super(SignUp, self).__init__(**kwargs)
        self.simple_view = True

    def get(self, request):
        super(SignUp, self).get(request)

        # Check if had signed in
        if request.user.is_authenticated():
            return redirect('/home/')

        self.context = Context(self.context)
        self.context.update(csrf(request))
        return render(request, 'signup.html', self.context)

    def post(self, request):
        super(SignUp, self).get(request)

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
        self.context.update({
            'noticeType': noticeType,
            'noticeTitle': noticeTitle,
            'noticeText': noticeText,
            'username': username,
            'password': password,
            'password_confirm': password_confirm,
        })
        self.context = Context(self.context)
        self.context.update(csrf(request))
        return render(request, 'signup.html', self.context)


class SignIn(BaseView):
    """ Sign in view """

    def __init__(self, **kwargs):
        super(SignIn, self).__init__(**kwargs)
        self.simple_view = True

    def get(self, request):
        super(SignIn, self).get(request)

        # Check if had signed in
        if request.user.is_authenticated():
            return redirect('/home/')

        self.context = Context(self.context)
        self.context.update(csrf(request))
        return render(request, 'login.html', self.context)

    def post(self, request):
        super(SignIn, self).get(request)

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
        self.context.update({
            'noticeType': noticeType,
            'noticeTitle': noticeTitle,
            'noticeText': noticeText,
            'username': username,
            'password': password,
        })
        self.context = Context(self.context)
        self.context.update(csrf(request))
        return render(request, 'login.html', self.context)


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
