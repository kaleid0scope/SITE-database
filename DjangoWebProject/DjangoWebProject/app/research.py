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
    
'''科研立项'''

#创建
def createResearchProject(request):
    if request.method == 'POST':
        error = []
        try:
            student = Students.objects.get(user = request.user)
            insp = Inspectors.objects.get(number = 10002)
        except Exception,e:
            error.append(e)
        form = CreateResearchProjectForm(request.POST)
        if form.is_valid():
            #try:
                cd = form.cleaned_data
                project = ResearchProjectRank(rankName = cd['ProjectName'],teacher = student,startingTime = cd['ProjectTime'],status = '待审核',rank = '',inspector = insp,)
                project.save()
                return render_with_type(request,'first.html',{'alert':'okkkk!'})
            #except Exception,e:
                error.append(e)
        else:
            error.append('Please input information of your project')
    else:
        form = CreateResearchProjectForm()
        error = None
    return render_with_type(request,'Create/createResearchProject.html',{'form':form,'alert':error})
#评价审核（审核结果输入）
def ResearchProject(request,id):
    try:  
        project = ResearchProjectRank.objects.get(id = int(id))
        auth = Students.objects.get(user = request.user).auth
        inspector = Inspectors.objects.get(user = request.user)
    except Exception,e:  
        return render_with_type(request,'ResearchProject.html',{'alert':e})
    if project.status == '待审核' and auth.isTeacher and auth.research:
        if request.method == 'POST':
            form = ResearchProjectForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                try:
                    choice = ChoicesTeam.objects.get(id = cd['level'])
                    project.rank = ChoicesTeam.objects.get(id = cd['level']).name
                    project.MemberScore = choice.memberScore
                    project.ManagerScore = choice.managerScore
                    project.memberComplete = choice.memberComplete
                    project.managerComplete = choice.managerComplete
                    if request.POST.has_key('passyes'):
                        project.status = '通过'
                    elif request.POST.has_key('passno'):
                        project.status = '未通过'
                    else :
                        return render_with_type(request,'ResearchProject.html',{'form':form,'project':project,'alert':'某还没命名的错误'})
                    project.inspector = inspector
                    project.save()
                    return render_with_type(request,'Index/ResearchProjectIndex.html',{'projects':ResearchProjectRank.objects.filter(status = '待审核'),'alert':'科研立项审核成功！','can':True})
                except Exception,e:  
                    error = e
            else:
                error = 'Please input information of your project'
        else:
            form = ResearchProjectForm()
            e = None
        return render_with_type(request,'ResearchProject.html',{'form':form,'project':project,'alert':e})
    elif auth.isTeacher and auth.ideologyConstruction:
       return render_with_type(request,'Index/ResearchProjectIndex.html',{'projects':ResearchProjectRank.objects.filter(status = '待审核'),'alert':'科研立项审核失败！该活动已审核','can':True})
    return render_with_type(request,'Index/ResearchProjectIndex.html',{'projects':ResearchProjectRank.objects.filter(status = '通过'),'can':False})
#项目详情
def ResearchProjectDetail(request,id):
    try:  
        project = ResearchProjectRank.objects.get(id = int(id))
    except Exception,e: 
        return render_with_type(request,'ResearchProjectDetail.html',{'alert':e})
    return render_with_type(request,'ResearchProjectDetail.html',{'project':project})
#申请加入
def JoinResearchProject(request,id):
    alert = ''
    try:  
        project = ResearchProjectRank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
    except Exception,e:  
        return render_with_type(request,'ResearchProjectDetail.html',{'alert':e})
    join = ResearchProject(status = '待审核',StudentNum = student ,rankNum = project , inspector = Inspectors.objects.get(number = 10002))
    join.save()
    alert = '成功加入！'
    return render_with_type(request,'Index/ResearchProjectIndex.html',{'alert':alert})
#申请者的列表
def ResearchProjectIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = ResearchProject.objects.filter(StudentNum= student)
    except Exception,e: 
        return render_with_type(request,'index.html',{'alert':e})
    if student.auth.isTeacher and student.auth.research:
        return render_with_type(request,'Index/researchProjectIndex.html',{'projects':ResearchProjectRank.objects.filter(status = '待审核'),'can':True})
    if project.count() == 0:
        return render_with_type(request,'Index/researchProjectIndex.html',{'projects':ResearchProjectRank.objects.filter(status = '通过'),'can':False})
    return render_with_type(request,'index.html',{'projects':ResearchProject.objects.filter(StudentNum = student),'alert':'您已加入科研立项!'})
#管理申请的列表
def ResearchProjectList(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = ResearchProjectRank.objects.get(teacher = student)
        joins = ResearchProject.objects.filter(rankNum = project)
    except Exception,e: 
        return render_with_type(request,'ResearchProjectList.html',{'alert':e})
    return render_with_type(request,'ResearchProjectList.html',{'projects':joins})
#申请者的详情
def ResearchProjectSDetail(request,id):
    try:  
        join = ResearchProject.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type(request,'ResearchProjectSDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        return render_with_type(request,'ResearchProjectSDetail.html',{'project':join,'student':student})
    return render_with_type(request,'ResearchProjectSDetail.html',{'alert':'您无权查看此报名信息！'})
#审核加入
def CheckResearchProject(request,id,isok):
    try:  
        join = ResearchProject.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type(request,'ResearchProjectSDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        if isok:
            join.status = '通过'
        else:
            join.status = '未通过'
        join.save()
    return render_with_type(request,'ResearchProjectSDetail.html',{'alert':'您无权审核此报名信息！'})

