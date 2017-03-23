# -*- coding: UTF-8 -*-

from django.shortcuts import render
from DjangoWebProject import settings
from django.http import HttpRequest
from django.template import RequestContext
from django.template.loader import get_template
from datetime import datetime
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from app.forms import *
from app.models import *
from app.type import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect  
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
import random,time
import uuid
import xlrd
import MySQLdb
from django.template.context import Context
'''import win32com.client as win32'''
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import DjangoWebProject.settings
    
def construction(request):
    return render_with_type(request,'app/construction.html')

'''校园活动'''

#创建
def createSchoolActivity(request):
    if request.method == 'POST':
        error = []
        try:
            student = Students.objects.get(user = request.user)
            insp = Inspectors.objects.get(number = 10002)
        except Exception,e:
            error.append(e)
        form = CreateSchoolActivityForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = SchoolActivityRank(rankName = cd['ProjectName'],
                                teacher = student,
                                startingTime = cd['startingTime'],
                                type = cd['type'],
                                sponsor = cd['sponsor'],
                                organizer = cd['organizer'],
                                awardLevel = cd['awardLevel'],
                                status = '待审核',
                               inspector = insp)
                project.save()
                return render_with_type(request,'first.html',{'alert':'okkkk!'})
            except Exception,e:
                error.append(e)
        else:
            error.append('Please input information of your project')
    else:
        form = CreateSchoolActivityForm()
        error = None
    return render_with_type(request,'Create/createSchoolActivity.html',{'form':form,'alert':error})
#评价审核（审核结果输入）
def schoolActivity(request,id):
    error = []
    try:  
        project = SchoolActivityRank.objects.get(id = int(id))
        auth = Students.objects.get(user = request.user).auth
        inspector = Inspectors.objects.get(user = request.user)
    except Exception,e:  
        error.append(e)
        return render_with_type(request,'SchoolActivity.html',{'alert':error})
    if project.status == '待审核':
        if request.method == 'POST':
            form = SchoolActivityForm(request.POST)
            if form.is_valid() and auth.isTeacher and auth.schoolActivity:
                cd = form.cleaned_data
                try:
                    choice = Choices.objects.get(id = cd['level'])
                    project.score = choice.score
                    project.complete = choice.complete
                    if request.POST.has_key('passyes'):
                        project.status = '通过'
                    elif request.POST.has_key('passno'):
                        project.status = '未通过'
                    project.inspector = inspector
                    project.save()
                    return render_with_type(request,'Index/SchoolActivityIndex.html',{'projects':SchoolActivityRank.objects.filter(status = '待审核'),'alert':'校园活动审核成功！','can':True})
                except Exception,e:  
                    error.append(e)
            else:
                error.append('Please input information of your project')
        else:
            form = SchoolActivityForm()
            return render_with_type(request,'Lecture.html',{'form':form,'project':project})
    elif auth.isTeacher and auth.schoolActivity:
       return render_with_type(request,'Index/SchoolActivityIndex.html',{'projects':SchoolActivityRank.objects.filter(status = '待审核'),'alert':'校园活动审核失败！该活动已审核','can':True})
    return render_with_type(request,'Index/SchoolActivityIndex.html',{'projects':SchoolActivityRank.objects.filter(status = '通过'),'can':False})
#项目详情
def SchoolActivityDetail(request,id):
    try:  
        project = SchoolActivityRank.objects.get(id = int(id))
    except Exception,e: 
        return render_with_type(request,'SchoolActivityDetail.html',{'alert':e})
    return render_with_type(request,'SchoolActivityDetail.html',{'project':project})
#申请加入
def JoinSchoolActivity(request,id):
    alert = ''
    try:  
        project = SchoolActivityRank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
    except Exception,e:  
        return render_with_type(request,'SchoolActivityDetail.html',{'alert':e})
    join = SchoolActivity(status = '待审核',StudentNum = student ,rankNum = project , inspector = Inspectors.objects.get(number = 10002))
    join.save()
    alert = '成功加入！'
    return render_with_type(request,'Index/SchoolActivityIndex.html',{'alert':alert})
#申请者的列表
def SchoolActivityIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = SchoolActivity.objects.filter(StudentNum= student)
    except Exception,e: 
        return render_with_type(request,'index.html',{'activities':SchoolActivity.objects.filter(StudentNum = student),'alert':e})
    if student.auth.isTeacher and student.auth.ideologyConstruction:
        return render_with_type(request,'Index/SchoolActivityIndex.html',{'projects':SchoolActivityRank.objects.filter(status = '待审核'),'can':True})
    return render_with_type(request,'Index/SchoolActivityIndex.html',{'projects':SchoolActivityRank.objects.filter(status = '通过'),'can':False})
#管理申请的列表
def SchoolActivityList(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = SchoolActivityRank.objects.get(teacher = student)
        joins = SchoolActivity.objects.filter(rankNum = project)
    except Exception,e: 
        return render_with_type(request,'SchoolActivityList.html',{'alert':e})
    return render_with_type(request,'SchoolActivityList.html',{'projects':joins})
#申请者的详情
def SchoolActivitySDetail(request,id):
    try:  
        join = SchoolActivity.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type(request,'SchoolActivitySDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        return render_with_type(request,'SchoolActivitySDetail.html',{'project':join,'student':student})
    return render_with_type(request,'SchoolActivitySDetail.html',{'alert':'您无权查看此报名信息！'})
#审核加入
def CheckSchoolActivityx(request,id,isok):
    try:  
        join = SchoolActivity.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type(request,'SchoolActivitySDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        if isok:
            join.status = '通过'
        else:
            join.status = '未通过'
        join.save()
    return render_with_type(request,'SchoolActivitySDetail.html',{'alert':'您无权审核此报名信息！'})

