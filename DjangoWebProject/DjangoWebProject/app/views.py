# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import AuthenticationForm
from app.forms import RegisterForm
from django.utils.translation import ugettext_lazy as _

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'SITE',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
         
def selecttype(request):
    usertypes = ['学生','老师','管理员']
    return render(request,'home.html',{'usertypes':usertypes})

def search_form(request):
    return render_to_response('search_form.html')

def search(request):
    if 'q' in request.GET:#GET是一个dict，使用文本框的name作为key
    #在这里需要做一个判断，是否存在提交数据，以免报错
        q = request.GET['q']
        #使用lookup后缀，意思为书名不区分大小写，包含q就可以
        users = User.objects.filter(username__icontains=q)
        return render_to_response('search_results.html', {'users' : users, 'query':q})
    else:
        message = 'You submitted an empty form.'
        #只是简单的返回一个response对象，因为没有使用模块，所以也不用渲染数据Context
        return HttpResponse(message)

def register(request):
    error = []
    if request.method == 'GET':
        return render_to_response('register.html')
    if request.method == 'POST':
        uf = RegisterForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            password2 = uf.cleaned_data['password2']
            email = uf.cleaned_data['email']
            type = uf.cleaned_data['type']
            if User.objects.all().filter(username=username):
                user = User()
                user.username = username
                user.set_password(password)
                user.email = email
                user.type = type
                user.save()
        return render_to_response('success.html', {'username': username})
    else:
        uf = RegisterForm()
    return render_to_response('fail.html',{'uf':uf,}, )
  
  