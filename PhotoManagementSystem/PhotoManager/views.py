# coding=utf-8
from django.conf.urls import include, url
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import *
from django.views.generic.edit import *
from django.contrib import auth
from django.template import Context, RequestContext
from django.template.context_processors import csrf
from PhotoManager.models import *
from config import *


class RestView(object):
    ''' Restful API for Model CRUD operation '''

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


class BaseView(View):
    def __init__(self, **kwargs):
        super(BaseView, self).__init__(**kwargs)
        self.context = {}

    def get(self, request):
        self.context = {}
        self.set_base(request)

    def set_gallery(self, request):
        photo_list = []
        for photo in Photo.objects.filter(album__user__username=request.user.username)[:5]:
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


class Home(BaseView):
    def get(self, request):
        super(Home, self).get(request)
        data = request.GET
        if 'noticeType' in data and 'noticeTitle' in data and 'noticeText' in data:
            self.context.update({
                'noticeType': data['noticeType'],
                'noticeTitle': data['noticeTitle'],
                'noticeText': data['noticeText'],
            })

        self.context = Context(self.context)
        self.context.update(csrf(request))
        print self.context
        return render(request, 'home.html', self.context)

    def post(self, request):
        print request
        return render(request, 'home.html', self.context)


class PhotoUpload(View):
    def get(self, request):
        print '000'
        return HttpResponse("1")

    def post(self, request):
        print request
        return HttpResponse("000")


def postTest(request):
    print request
    return HttpResponse("000")


class TimeLine(BaseView):
    def get(self, request):
        super(TimeLine, self).get(request)
        self.context = Context(self.context)
        self.context.update(csrf(request))
        print self.context
        return render(request, '', self.context)


class SignUp(View):
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/home/')
        context = Context({})
        context.update(csrf(request))
        return render(request, 'signup.html', context)

    def post(self, request):
        # print request.POST
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if len(username) < 3:
            noticeText = '用户名长度至少3位'
        elif User.objects.filter(username=username):
            noticeText = '您选择的用户名已被使用'
        elif len(password) < 6:
            noticeText = '密码长度至少6位'
        elif password != password_confirm:
            noticeText = '两次密码输入不一致'
        else:
            User.objects.create_user(username=username, password=password)
            noticeType = 'success'
            noticeTitle = '注册成功'
            noticeText = ' '
            return HttpResponseRedirect(
                '/signin/?noticeType=%s&noticeTitle=%s&noticeText=%s' % (noticeType, noticeTitle, noticeText))

        # Sign up fail, return warning info
        noticeType = 'warn'
        noticeTitle = '注册失败'
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
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/home/')
        data = request.GET
        if 'noticeType' in data and 'noticeTitle' in data and 'noticeText' in data:
            context = Context({
                'noticeType': data['noticeType'],
                'noticeTitle': data['noticeTitle'],
                'noticeText': data['noticeText'],
            })
        else:
            context = Context({})
        context.update(csrf(request))
        return render(request, 'login.html', context)

    def post(self, request):
        # print request.POST
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                noticeType = 'success'
                noticeTitle = '登录成功'
                noticeText = ' '
                return HttpResponseRedirect(
                    '/home/?noticeType=%s&noticeTitle=%s&noticeText=%s' % (noticeType, noticeTitle, noticeText))
            else:
                noticeText = '账户被禁用'
        else:
            noticeText = '用户名和密码不匹配'

        # Log in fail
        noticeType = 'warn'
        noticeTitle = '登录失败'
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
    def get(self, request):
        auth.logout(request)
        noticeType = 'success'
        noticeTitle = '已退出登录'
        noticeText = ' '
        return HttpResponseRedirect(
            '/signin/?noticeType=%s&noticeTitle=%s&noticeText=%s' % (noticeType, noticeTitle, noticeText))


class Test(View):
    def get(self, request):
        context = Context(request.GET)
        context.update(csrf(request))
        return render(request, request.GET['v'] + '.html', context)
