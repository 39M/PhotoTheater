# coding=utf-8
from django.conf.urls import include, url
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import *
from django.views.generic.edit import *
from django.contrib import auth
from django.template import Context
from django.template.context_processors import csrf
from PhotoManager.models import User, Album, Photo, Comment


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


def gallery(request):
    context_extras = {
        'SlideShow': [
            # Images info
        ]
    }
    return context_extras


def side_bar(request):
    context_extras = {
        'runTime': {
            'ViewName': ''
        }
    }

    context_extras.update(gallery(request))
    return context_extras


def nav_bar(request):
    context_extras = {
        'user': {

        }
    }
    return context_extras


def base(request):
    context_extras = {
        'CONFIG': {
            'SITE': {
                'TITLE': 'WEBSITE_TITLE'
            },
        }
    }

    context_extras.update(side_bar(request))
    context_extras.update(nav_bar(request))
    return context_extras


class Home(View):
    def get(self, request):
        context = {

        }
        data = request.GET
        if 'noticeType' in data and 'noticeTitle' in data and 'noticeText' in data:
            context.update({
                'noticeType': data['noticeType'],
                'noticeTitle': data['noticeTitle'],
                'noticeText': data['noticeText'],
            })

        context.update(csrf(request))
        return render(request, 'home.html', context)

    def post(self, request):
        context = {

        }
        return render(request, 'home.html', context)


class Index(View):
    def get(self, request):
        return HttpResponse('Index')


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
        noticeType = ''
        noticeTitle = ''
        noticeText = ''
        fail = False

        if len(username) < 3:
            noticeType = 'warn'
            noticeTitle = '注册失败'
            noticeText = '用户名长度至少3位'
            fail = True

        if not fail and User.objects.filter(username=username):
            noticeType = 'warn'
            noticeTitle = '注册失败'
            noticeText = '您选择的用户名已被使用'
            fail = True

        if not fail and len(password) < 6:
            noticeType = 'warn'
            noticeTitle = '注册失败'
            noticeText = '密码长度至少6位'
            fail = True

        if not fail and password != password_confirm:
            noticeType = 'warn'
            noticeTitle = '注册失败'
            noticeText = '两次密码输入不一致'
            fail = True

        if fail:
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

        User.objects.create_user(username=username, password=password)
        noticeType = 'success'
        noticeTitle = '注册成功'
        noticeText = '请登录后使用'
        return HttpResponseRedirect(
            '/signin/?noticeType=%s&noticeTitle=%s&noticeText=%s' % (noticeType, noticeTitle, noticeText))


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
        noticeType = ''
        noticeTitle = ''
        noticeText = ''

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
                noticeType = 'warn'
                noticeTitle = '登录失败'
                noticeText = '账户被禁用'
        else:
            noticeType = 'warn'
            noticeTitle = '登录失败'
            noticeText = '用户名和密码不匹配'

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
        return HttpResponse('SignOut get')


class Test(View):
    def get(self, request):
        context = Context(request.GET)
        context.update(csrf(request))
        return render(request, request.GET['v'] + '.html', context)
