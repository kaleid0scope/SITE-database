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
'''思建活动'''

#创建
def createIdeologyConstruction(request):
    if request.method == 'POST':
        error = []
        try:
            student = Students.objects.get(user = request.user)
            insp = Inspectors.objects.get(number = 10002)
        except Exception,e:
            error.append(e)
        form = CreateIdeologyConstructionForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = IdeologyConstructionRank(rankName = cd['ProjectName'],
                                type = cd['type'],
                                teacher = student,
                                startingTime = cd['startingTime'],
                                organizer = cd['organizer'],
                                Location = cd['Location'],
                                Content = cd['Content'],
                                status = '待审核',
                               inspector = insp,)
                project.save()
                return render_with_type(request,'first.html',{'alert':'okkkk!'})
            except Exception,e:
                error.append(e)
        else:
            error.append('Please input information of your project')
    else:
        form = CreateIdeologyConstructionForm()
        error = None
    return render_with_type(request,'Create/createIdeologyConstruction.html',{'form':form,'alert':error})
#评价审核（审核结果输入）
def ideologyConstruction(request,id):
    error = []
    try:  
        project = IdeologyConstructionRank.objects.get(id = int(id))
        auth = Students.objects.get(user = request.user).auth
        inspector = Inspectors.objects.get(user = request.user)
    except Exception,e:  
        error.append(e)
        return render_with_type(request,'IdeologyConstruction.html',{'alert':error})
    if project.status == '未通过':
        if request.method == 'POST':
            form = IdeologyConstructionForm(request.POST)
            if form.is_valid() and auth.isTeacher and auth.ideologyConstruction:
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
                    return render_with_type(request,'Index/IdeologyConstructionIndex.html',{'projects':IdeologyConstructionRank.objects.filter(status = '待审核'),'alert':'思建活动审核成功！','can':True})
                except Exception,e:  
                    error.append(e)
            else:
                error.append('Please input information of your project')
        else:
            form = IdeologyConstructionForm()
            return render_with_type(request,'IdeologyConstruction.html',{'form':form,'project':project})
    elif auth.isTeacher and auth.ideologyConstruction:
       return render_with_type(request,'Index/IdeologyConstructionIndex.html',{'projects':IdeologyConstructionRank.objects.filter(status = '待审核'),'alert':'思建活动审核失败！该活动已审核','can':True})
    return render_with_type(request,'Index/IdeologyConstructionIndex.html',{'projects':IdeologyConstructionRank.objects.filter(status = '通过'),'can':False})
#项目详情
def IdeologyConstructionDetail(request,id):
    try:  
        project = IdeologyConstructionRank.objects.get(id = int(id))
    except Exception,e: 
        return render_with_type(request,'IdeologyConstructionDetail.html',{'alert':e})
    return render_with_type(request,'IdeologyConstructionDetail.html',{'project':project})
#申请加入
def JoinIdeologyConstruction(request,id):
    alert = ''
    try:  
        project = IdeologyConstructionRank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
    except Exception,e:  
        return render_with_type(request,'IdeologyConstructionDetail.html',{'alert':e})
    join = IdeologyConstruction(status = '待审核',StudentNum = student ,rankNum = project , inspector = Inspectors.objects.get(number = 10002))
    join.save()
    alert = '成功加入！'
    return render_with_type(request,'Index/IdeologyConstructionIndex.html',{'alert':alert})
#申请者的列表
def IdeologyConstructionIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = IdeologyConstruction.objects.filter(StudentNum= student)
    except Exception,e: 
        return render_with_type(request,'index.html',{'constructions':IdeologyConstruction.objects.filter(StudentNum = student),'alert':e})
    if student.auth.isTeacher and student.auth.ideologyConstruction:
        return render_with_type(request,'Index/IdeologyConstructionIndex.html',{'projects':IdeologyConstructionRank.objects.filter(status = '待审核'),'can':True})
    return render_with_type(request,'Index/IdeologyConstructionIndex.html',{'projects':IdeologyConstructionRank.objects.filter(status = '通过'),'can':False})
#管理申请的列表
def IdeologyConstructionList(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = IdeologyConstructionRank.objects.get(teacher = student)
        joins = IdeologyConstruction.objects.filter(rankNum = project)
    except Exception,e: 
        return render_with_type(request,'IdeologyConstructionList.html',{'alert':e})
    return render_with_type(request,'IdeologyConstructionList.html',{'projects':joins})
#申请者的详情
def IdeologyConstructionSDetail(request,id):
    try:  
        join = IdeologyConstruction.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type(request,'IdeologyConstructionSDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        return render_with_type(request,'IdeologyConstructionSDetail.html',{'project':join,'student':student})
    return render_with_type(request,'IdeologyConstructionSDetail.html',{'alert':'您无权查看此报名信息！'})
#审核加入
def CheckIdeologyConstructions(request,id,isok):
    try:  
        join = IdeologyConstruction.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type(request,'IdeologyConstructionSDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        if isok:
            join.status = '通过'
        else:
            join.status = '未通过'
        join.save()
    return render_with_type(request,'IdeologyConstructionSDetail.html',{'alert':'您无权审核此报名信息！'})

    