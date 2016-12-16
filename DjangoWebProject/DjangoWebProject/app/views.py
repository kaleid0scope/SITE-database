# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from app.forms import ResetPasswordForm
from app.forms import CreateResearchProjectForm,JoinResearchProjectForm
from app.forms import RegisterForm,ChangepwdForm,ChangeauthForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect  
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from app.models import Students,Authorizations,Inspectors
from app.models import ResearchProject,ResearchProjectRank
import random,time

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/index.html',
        {
            'title':'SITE',
            'year':datetime.now().year,
        })

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
"""def register(request):
     assert isinstance(request, HttpRequest)
     return render(
         request,
         'app/register.html',
         {'title':'register',
          'message':'add your message',
          'year':datetime.now().year,
          }
         )"""
         
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

def reset(request):
    #可以不写，因为python中if中定义的变量，也可以在整个函数中可见
    form = None 
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.filter(username=cd['username'],email=cd['email'])
            if user is not None:
                user.update(password=make_password(cd['password']))
                return HttpResponseRedirect('/login')
    else:
        form = ResetPasswordForm()
    return render_to_response('reset_form.html', {'form': form})

def changepassword(request,username):
	error = []
	if request.method == 'POST':
		form = ChangepwdForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			user = authenticate(username=username,password=data['old_pwd'])
			if user is not None:
				if data['new_pwd'] == data['new_pwd2']:
					newuser = User.objects.get(username__exact=username)
					newuser.set_password(data['new_pwd'])
					newuser.save()
					return HttpResponseRedirect('/login/')
				else:
					error.append('Please input the same password')
			else:
				error.append('Please correct the old password')
		else:
			error.append('Please input the required domain')
	else:
		form = ChangepwdForm()
	return render_to_response('changepassword.html',{'form':form,'error':error})

def changeauth(request,username):
	error = []
	if request.method == 'POST':
		form = ChangeauthForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			nowuser = request.user
			if nowuser is not None:
				if nowuser.is_superuser:
				    user = User.objects.get(username__exact=username)
				    auth = Students.objects.get(user__exact=user.id).auth
				    auth.isTeacher = data['isTeacher']
				    auth.research = data['research']
				    auth.paper = data['paper']
				    auth.competition = data['competition']
				    auth.exchange = data['exchange']
				    auth.ideologyConstruction = data['ideologyConstruction']
				    auth.lecture = data['lecture']
				    auth.volunteering = data['volunteering']
				    auth.schoolActivity= data['schoolActivity']
				    auth.internship = data['internship']
				    auth.studentCadre = data['studentCadre']
				    auth.save()
				    return HttpResponseRedirect('/admin/app/students')
				else:
				    error.append('错误的请求：管理员身份验证未通过')
			else:
				error.append('错误的请求：请先登录')
		else:
			error.append('Please input the required domain')
	else:
		form = ChangeauthForm()
	return render_to_response('changeauth.html',{'form':form,'error':error,'username':username})

"""cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                ['siteowner@example.com'],
            )"""

def createResearchProject(request):
    error = []
    if request.method == 'POST':
        form = CreateResearchProjectForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = ResearchProjectRank(rankName = cd['ProjectName'],teacherNum = Students.objects.get(user = request.user),startingTime = cd['ProjectTime'],status = 1,rank = '',ManagerScore = 0,MemberScore = 0,CompleteNum = 0,inspectorNum = Inspectors.objects.get(inspectorNum = 10002))
            if True:
                project.save()
                return HttpResponse('科研立项项目创建成功！')
            else:
                error.append('Please check your importation')
        else:
            error.append('Please input information of your project')
    else:
        form = CreateResearchProjectForm()
    return render_to_response('createResearchProject.html',{'form':form,'error':error})