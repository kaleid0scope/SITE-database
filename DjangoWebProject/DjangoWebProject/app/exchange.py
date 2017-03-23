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



'''交换项目'''

def createExchange(request):
    if request.method == 'POST':
        error = []
        #try:
        student = Students.objects.get(user = request.user)
        insp = Inspectors.objects.get(number = 10002)
        #except Exception,e:#error.append(e)
        form = CreateExchangeForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = ExchangeRank(rankName = cd['ProjectName'],
                                type = cd['type'],
                                nature = cd['nature'],
                                student = student,
                                startTime = cd['startTime'],
                                endTime = cd['endTime'],
                                status = '待审核',
                                
                                
                               inspector = insp,)
                project.save()
                return render_with_type(request,'first.html',{'alert':'okkkk!'})
            except Exception,e:
                error.append(e)
        else:
            error.append('Please input information of your project')
    else:
        form = CreateExchangeForm()
        error = None
    return render_with_type(request,'Create/createExchange.html',{'form':form,'alert':error})
def exchange(request,id):
    error = []
    try:  
        project = ExchangeRank.objects.get(id = int(id))
        auth = Students.objects.get(user = request.user).auth
        inspector = Inspectors.objects.get(user = request.user)
    except Exception,e:  
        error.append(e)
        return render_with_type(request,'Exchange.html',{'alert':error})
    if project.status == '待审核' and auth.isTeacher and auth.exchange:
        if request.method == 'POST':
            form = ExchangeForm(request.POST)
            if form.is_valid():
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
                    return render_with_type(request,'Index/ExchangeIndex.html',{'projects':ExchangeRank.objects.filter(status = '待审核'),'alert':'审核成功！','can':True})
                except Exception,e:  
                    error.append(e)
            else:
                error.append('Please input information of your project')
        else:
            form = ExchangeForm()
        return render_with_type(request,'Exchange.html',{'form':form,'project':project})
    elif auth.isTeacher and auth.ideologyConstruction:
       return render_with_type(request,'Index/ExchangeIndex.html',{'projects':ExchangeRank.objects.filter(status = '待审核'),'alert':'审核失败！该活动已审核','can':True})
    return render_with_type(request,'Index/ExchangeIndex.html',{'projects':ExchangeRank.objects.filter(status = '通过'),'can':False})
def exchangeIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = ExchangeRank.objects.filter(student = student.StudentNum)
    except Exception,e: 
        return render_with_type(request,'index.html',{'alert':e})
    if student.auth.isTeacher and student.auth.lecture:
        return render_with_type(request,'Index/ExchangeIndex.html',{'projects':ExchangeRank.objects.filter(status = '待审核')})#teacher
    return render_with_type(request,'index.html',{'alert':'你没有权限审核论文！请与管理员联系'})

