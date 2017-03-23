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
    
def construction(request):
    return render_with_type(request,'app/construction.html')


'''ʵ??ʵϰ
'''
#????
def createInternship(request):
    if request.method == 'POST':
        error = []
        try:
            student = Students.objects.get(user = request.user)
            insp = Inspectors.objects.get(number = 10002)
        except Exception,e:
            error.append(e)
        form = CreateInternshipForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = InternshipRank(rankName = cd['ProjectName'],
                                teacher = Students.objects.get(user = request.user),
                                InternshipTime = cd['startingTime'],
                                type = cd['type'],
                                status = '??????',
                                inspector = Inspectors.objects.get(number = 10002))
                project.save()
                return render_with_type(request,'first.html',{'alert':'okkkk!'})
            except Exception,e:
                error.append(e)
        else:
            error.append('Please input information of your project')
    else:
        form = CreateInternshipForm()
        error = None
    return render_with_type(request,'Create/createInternship.html',{'form':form,'alert':error})
#???????ˣ????˽??????룩
def internship(request,id):
    error = []
    try:  
        project = InternshipRank.objects.get(id = int(id))
        auth = Students.objects.get(user = request.user).auth
        inspector = Inspectors.objects.get(user = request.user)
    except Exception,e:  
        error.append(e)
        return render_with_type(request,'Verify/Internship.html',{'alert':error})
    if project.status == '??????':
        if request.method == 'POST':
            form = InternshipForm(request.POST)
            if form.is_valid() and auth.isTeacher and auth.internship:
                cd = form.cleaned_data
                try:
                    choice = Choices.objects.get(id = cd['level'])
                    project.score = choice.score
                    project.complete = choice.complete
                    if request.POST.has_key('passyes'):
                        project.status = 'ͨ??'
                    elif request.POST.has_key('passno'):
                        project.status = 'δͨ??'
                    project.inspector = inspector
                    project.save()
                    return render_with_type(request,'Index/InternshipIndex.html',{'projects':InternshipRank.objects.filter(status = '??????'),'alert':'ʵ??ʵϰ???˳ɹ???','can':True})
                except Exception,e:  
                    error.append(e)
            else:
                error.append('Please input information of your project')
        else:
            form = InternshipForm()
            return render_with_type(request,'Verify/Internship.html',{'form':form,'project':project})
    elif auth.isTeacher and auth.internship:
       return render_with_type(request,'Index/InternshipIndex.html',{'projects':InternshipRank.objects.filter(status = '??????'),'alert':'ʵ??ʵϰ????ʧ?ܣ??û??????','can':True})
    return render_with_type(request,'Index/InternshipIndex.html',{'projects':InternshipRank.objects.filter(status = 'ͨ??'),'can':False})
#??Ŀ????
def InternshipDetail(request,id):
    try:  
        project = InternshipRank.objects.get(id = int(id))
    except Exception,e: 
        return render_with_type(request,'InternshipDetail.html',{'alert':e})
    return render_with_type(request,'InternshipDetail.html',{'project':project})
#????????
def JoinInternship(request,id):
    alert = ''
    try:  
        project = InternshipRank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
    except Exception,e:  
        return render_with_type(request,'InternshipDetail.html',{'alert':e})
    join = Internship(status = '??????',StudentNum = student ,rankNum = project , inspector = Inspectors.objects.get(number = 10002))
    join.save()
    alert = '?ɹ????룡'
    return render_with_type(request,'Index/InternshipIndex.html',{'alert':alert})
#?????ߵ??б?
def InternshipIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = Internship.objects.filter(StudentNum= student)
    except Exception,e: 
        return render_with_type(request,'index.html',{'internships':Internship.objects.filter(StudentNum = student),'alert':e})
    if student.auth.isTeacher and student.auth.ideologyConstruction:
        return render_with_type(request,'Index/InternshipIndex.html',{'projects':InternshipRank.objects.filter(status = '??????'),'can':True})
    return render_with_type(request,'Index/InternshipIndex.html',{'projects':InternshipRank.objects.filter(status = 'ͨ??'),'can':False})
#???????????б?
def InternshipList(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = InternshipRank.objects.get(teacher = student)
        joins = Internship.objects.filter(rankNum = project)
    except Exception,e: 
        return render_with_type(request,'InternshipList.html',{'alert':e})
    return render_with_type(request,'InternshipList.html',{'projects':joins})
#?????ߵ?????
def InternshipSDetail(request,id):
    try:  
        join = Internship.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type(request,'InternshipSDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        return render_with_type(request,'InternshipSDetail.html',{'project':join,'student':student})
    return render_with_type(request,'InternshipSDetail.html',{'alert':'????Ȩ?鿴?˱?????Ϣ??'})
#???˼???
def CheckInternship(request,id,isok):
    try:  
        join = Internship.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type(request,'InternshipSDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        if isok:
            join.status = 'ͨ??'
        else:
            join.status = 'δͨ??'
        join.save()
    return render_with_type(request,'InternshipSDetail.html',{'alert':'????Ȩ???˴˱?????Ϣ??'})