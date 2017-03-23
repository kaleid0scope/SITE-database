# -*- coding: utf-8 -*-

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

'''志愿活动'''

#创建
def createVolunteering(request):
    if request.method == 'POST':
        error = []
        try:
            student = Students.objects.get(user = request.user)
            insp = Inspectors.objects.get(number = 10002)
        except Exception,e:
            error.append(e)
        form = CreateVolunteeringForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = VolunteeringRank(rankName = cd['ProjectName'],
                                teacher = Students.objects.get(user = request.user),
                                startingTime = cd['startingTime'],
                                volunteerTime = cd['volunteerTime'],
                                organizer = cd['organizer'],
                                Location = cd['Location'],
                                Content = cd['Content'],
                                status = '待审核',
                                inspector = Inspectors.objects.get(number = 10002))
                project.save()
                return render_with_type(request,'first.html',{'alert':'okkkk!'})
            except Exception,e:
                error.append(e)
        else:
            error.append('Please input information of your project')
    else:
        form = CreateVolunteeringForm()
        error = None
    return render_with_type(request,'Create/createVolunteering.html',{'form':form,'alert':error})
#评价审核（审核结果输入）
def volunteering(request,id):
    error = []
    try:  
        project = VolunteeringRank.objects.get(id = int(id))
        auth = Students.objects.get(user = request.user).auth
        inspector = Inspectors.objects.get(user = request.user)
    except Exception,e:  
        error.append(e)
        return render_with_type(request,'Volunteering.html',{'alert':error})
    if project.status == '待审核':
        if request.method == 'POST':
            form = VolunteeringForm(request.POST)
            if form.is_valid() and auth.isTeacher and auth.volunteering:
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
                    return render_with_type(request,'Index/VolunteeringIndex.html',{'projects':VolunteeringRank.objects.filter(status = '待审核'),'alert':'志愿活动审核成功！','can':True})
                except Exception,e:  
                    error.append(e)
            else:
                error.append('Please input information of your project')
        else:
            form = VolunteeringForm()
            return render_with_type(request,'Lecture.html',{'form':form,'project':project})
    elif auth.isTeacher and auth.volunteering:
       return render_with_type(request,'Index/VolunteeringIndex.html',{'projects':VolunteeringRank.objects.filter(status = '待审核'),'alert':'志愿活动审核失败！该活动已审核','can':True})
    return render_with_type(request,'Index/VolunteeringIndex.html',{'projects':VolunteeringRank.objects.filter(status = '通过'),'can':False})
#项目详情
def VolunteeringDetail(request,id):
    try:  
        project = VolunteeringRank.objects.get(id = int(id))
    except Exception,e: 
        return render_with_type(request,'VolunteeringDetail.html',{'alert':e})
    return render_with_type(request,'VolunteeringDetail.html',{'project':project})
#申请加入
def JoinVolunteering(request,id):
    alert = ''
    try:  
        project = VolunteeringRank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
    except Exception,e:  
        return render_with_type(request,'VolunteeringDetail.html',{'alert':e})
    join = Volunteering(status = '待审核',StudentNum = student ,rankNum = project , inspector = Inspectors.objects.get(number = 10002))
    join.save()
    alert = '成功加入！'
    return render_with_type(request,'Index/VolunteeringIndex.html',{'alert':alert})
#申请者的列表
def VolunteeringIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = Volunteering.objects.filter(StudentNum= student)
    except Exception,e: 
        return render_with_type(request,'index.html',{'volunteerings':Volunteering.objects.filter(StudentNum = student),'alert':e})
    if student.auth.isTeacher and student.auth.ideologyConstruction:
        return render_with_type(request,'Index/VolunteeringIndex.html',{'projects':VolunteeringRank.objects.filter(status = '待审核'),'can':True})
    return render_with_type(request,'Index/VolunteeringIndex.html',{'projects':VolunteeringRank.objects.filter(status = '通过'),'can':False})
#管理申请的列表
def VolunteeringList(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = VolunteeringRank.objects.get(teacher = student)
        joins = Volunteering.objects.filter(rankNum = project)
    except Exception,e: 
        return render_with_type(request,'VolunteeringList.html',{'alert':e})
    return render_with_type(request,'VolunteeringList.html',{'projects':joins})
#申请者的详情
def VolunteeringSDetail(request,id):
    try:  
        join = Volunteering.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type(request,'VolunteeringSDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        return render_with_type(request,'VolunteeringSDetail.html',{'project':join,'student':student})
    return render_with_type(request,'VolunteeringSDetail.html',{'alert':'您无权查看此报名信息！'})
#审核加入
def CheckVolunteeringx(request,id,isok):
    try:  
        join = Volunteering.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type(request,'VolunteeringSDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        if isok:
            join.status = '通过'
        else:
            join.status = '未通过'
        join.save()
    return render_with_type(request,'VolunteeringSDetail.html',{'alert':'您无权审核此报名信息！'})

