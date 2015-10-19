from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.contrib import auth
from PhotoManager.models import User, Album, Photo, Comment

class Index(View):
    def get(self, request):
        return HttpResponse('Index')


class SignUp(View):
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponse('Signed In')
        return HttpResponse('SignUp get')

    def post(self, request):
        username = request.POST['username']
        if User.objects.filter(username=username):
            return HttpResponse('User exist')

        password = request.POST['password']
        if len(password) < 6:
            return HttpResponse('Password too short')

        password_repeat = request.POST['password_repeat']
        if password != password_repeat:
            return HttpResponse('Password error')

        User.objects.create_user(username=username, password=password)
        return HttpResponse('SignUp post')


class SignIn(View):
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponse('Signed In')
        return HttpResponse('SignIn get')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponse('Sign in success')
            else:
                return HttpResponse('Account disabled')
        else:
            return HttpResponse('Invalid sign in')


class SignOut(View):
    def get(self, request):
        auth.logout(request)
        return HttpResponse('SignOut get')
