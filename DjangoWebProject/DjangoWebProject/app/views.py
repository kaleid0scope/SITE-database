# -*- coding: utf-8 -*-

from django.shortcuts import render
from DjangoWebProject import settings
from django.http import HttpRequest
from django.template import RequestContext
from django.template.loader import get_template
from datetime import datetime
from django.shortcuts import *
from django.contrib.auth.models import User
from app.forms import *
from app.models import *
from app.Info import *
from app.project import *
from app.complete import GetComplete
from django.http import HttpResponse
from django.http import HttpResponseRedirect  
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import * 
import random,time
import MySQLdb
from django.template.context import Context
import sys
from django.core.files.uploadedfile import TemporaryUploadedFile
import os
from deco import *
from app.excel import *
from django.contrib.contenttypes.models import ContentType
reload(sys)
sys.setdefaultencoding("utf-8")
import DjangoWebProject.settings

def NewWeb():
    if not Permission.objects.filter(codename = 'is_instructor'): 
        Permission.objects.create(name=u'是否为辅导员',content_type = ContentType.objects.get_for_model(User),codename='is_instructor')
    user = User.objects.filter()

@teacher_required
def Excel(request,linkid = None):
    if request.method == 'POST' and request.POST.has_key('register'):
        myFile = request.FILES.get("register", None)    # 获取上传的文件，如果没有文件，则默认为None  
        if not myFile:  
            return HttpResponse("no files for upload!") 
        if ExcelRegister(myFile.temporary_file_path()):
            return HttpResponse("over!")  
        return HttpResponse("error")
    elif request.method == 'POST' and request.POST.has_key('lesson'):
        myFile = request.FILES.get("lesson", None)
        if not myFile:  
            return HttpResponse("no files for upload!") 
        if ExcelImportLesson(myFile.temporary_file_path()):
            return HttpResponse("over!")  
        return HttpResponse("error")
    elif request.method == 'POST' and request.POST.has_key('link'):
        myFile = request.FILES.get("link", None)
        if not myFile:  
            return HttpResponse("no files for upload!") 
        if linkid != None:
          if getType(request) != '管理员':
            instructor = Instructor.objects.get(user = request.user)
            if Major.objects.filter(instructor = instructor).filter(pk = link.student.major.pk):
                if ExcelImportLink(myFile.temporary_file_path(),linkid):
                    return HttpResponse("over!")  
        return HttpResponse("error")
    else:
        assert isinstance(request, HttpRequest)
        return render(request,'app/excel.html',{})

def ShowComplete(request,id = None):
    if getType(request) in ('管理员','教师端'):
        if id != None:student = Students.objects.get(pk = id)
        else:return StudentList(request)
    elif getType(request) == '学生端':student = Students.objects.get(user = request.user)
    else: return Error(request,u'您无权访问')
    complete = GetComplete(request,student)
    fields = Complete._meta.fields
    FieldProject = {}
    for field in fields :
        if field.name != 'id': FieldProject[field.verbose_name] = getattr(complete,field.name) #键值对
    return render(request,'complete.html', {'FPS': FieldProject})

def StudentList(request):
    if getType(request) == '教师端':
        instructor = Instructor.objects.get(user = request.user)
        majors = Major.objects.filter(instructor = instructor)
        students = Students.objects.filter(major__in = majors)
    elif getType(request) == '管理员':
        students = Students.objects.all()
    else: return Error(request,u'您无权访问')
    return render(request,'studentList.html', {'students': students})
    
def construction(request):
    return render(request,'app/construction.html',{})

def home(request):
    NewWeb()
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated():
        return render(request,'app/index.html',{})
    else:
        return redirect('/login')

def first(request):
    return render(request,'first.html')

def shit(request):
    return render(request,'app/shit.html',{})

def contact(request):
    return render(request,'app/contact.html', {'t': settings.STATIC_ROOT})

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

def search_form(request):
    return render(request,'search_form.html',{})

def search(request):
    if 'q' in request.GET:#GET是一个dict，使用文本框的name作为key
    #在这里需要做一个判断，是否存在提交数据，以免报错
        q = request.GET['q']
        #使用lookup后缀，意思为书名不区分大小写，包含q就可以
        users = User.objects.filter(username__icontains=q)
        return render(request,'search_results.html', {'users' : users, 'query':q})
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
            try:
                student = Students.objects.get(user = User.objects.get(username=cd['username'],email=cd['email']))
            except Exception,e:
                return render(request,'reset_form.html', {'form': form,'alert':e})
            if student.StudentNum == cd['StudentNum'] and str(student.identityNumber)[-6:] == cd['IdentityNumberSix']:
                user.password = make_password(cd['password'])
                return HttpResponseRedirect('/login')
    else:
        form = ResetPasswordForm()
    return render(request,'reset_form.html', {'form': form})

def changepassword(request,username):
	error = None
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
	return render(request,'changepassword.html',{'form':form,'alert':error})


def index(request):
    alert = 'unlogin!'
    if request.user.is__authenticated():
        try:
            student = Students.objects.get(user = request.user)
            return render(request,'index.html',{'projects':ResearchProject.objects.filter(StudentNum = student),
                                            'constructions':IdeologyConstruction.objects.filter(StudentNum = student),
                                            'lectures':Lecture.objects.filter(StudentNum = student),
                                            'volunteerings':Volunteering.objects.filter(StudentNum = student),
                                            'activities':SchoolActivity.objects.filter(StudentNum = student),
                                            'internships':Internship.objects.filter(StudentNum = student),
                                            'cadres':StudentCadreRank.objects.filter(StudentNum = student),
                                            'papers':PaperRank.objects.filter(StudentNum = student),
                                            'exchanges':ExchangeRank.objects.filter(StudentNum = student),
                                            'competitions':CompetitionRank.objects.filter(StudentNum = student)})
        except Exception,e:
            alert = 'unregister!'
    return render_to_response('/home',{'alert':alert})