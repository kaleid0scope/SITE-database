# -*- coding: utf-8 -*-

from app.forms import *
from app.models import *
from app.type import *
from app.Info import *
from app.project import *
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from DjangoWebProject import settings
from django.http import HttpRequest
from django.template import RequestContext
from django.template.loader import get_template

def ProjectDetail(rank,link,request,id):
    try:  
        project = rank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
        links = link.objects.filter(rankNum = project).filter(status = '通过') #已加入的关系
        joins = link.objects.filter(rankNum = project).filter(status = '待审核') #待审核的关系
        members = []
        for link in links:
            members.append(link.StudentNum) #所有已加入的成员
        members.insert(0,student)
    except Exception,e: 
        return render_with_type(request,'{name}Detail.html'.format(name = link._meta.object_name),{'alert':e})
    if project.teacher == student: #如果为项目的管理者
        alert = None
        if request.method == 'POST':
            try:
                num = request.GET.get('num','')
                joiner = Students.objects.get(StudentNum = num)
                joinlink = link.objects.filter(rankNum = project).get(StudentNum = joiner)
            except Exception,e: 
                return render_with_type(request,'{name}Detail.html'.format(name = link._meta.object_name),{'alert':e})
            if request.POST.has_key('passyes'):
                joinlink.status = '通过'
            elif request.POST.has_key('passno'):
                joinlink.status = '未通过'
            joinlink.save()
            alert = '审核成功！' 
        return render_with_type(request,'{name}Detail.html'.format(name = link._meta.object_name),
            {'project':project,'hasJoin':True,'members':members,'manage':True,'joiners':joins,'alert':alert})
    elif members.count(student) == 1: #如果为该项目已通过的成员
        return render_with_type(request,'{name}Detail.html'.format(name = link._meta.object_name),{'project':project,'hasJoin':True,'members':members})
    return render_with_type(request,'{name}Detail.html'.format(name = link._meta.object_name),{'project':project})

def ProjectIndex(rank,link,request):
    try:  
        student = Students.objects.get(user = request.user)
        links = link.objects.filter(StudentNum = student) #所有加入的项目
        created = rank.objects.filter(teacher = student)
        joined = []
        for link in links:
            joined.append(link.rankNum)
    except Exception,e: 
        return render_with_type(request,'app/login.html',{'alert':e})
    if student.auth.isTeacher and student.auth.ideologyConstruction: #如果是教师，返回待审核的项目
        return render_with_type(request,'Index/{name}Index.html'.format(name = link._meta.object_name),
            {'projects':rank.objects.filter(status = '待审核'),'can':True})
    else :  #否则，返回各类项目
        return render_with_type(request,'Index/{name}Index.html'.format(name = link._meta.object_name),
            {'projects':rank.objects.filter(status = '通过'),
            'Cprojects':created,
            'Jprojects':joined,
            'can':False})

def ProjectCheck(rank,link,f,request,id):
    error = None
    try:  
        project = rank.objects.get(id = int(id))
        auth = Students.objects.get(user = request.user).auth
        inspector = Inspectors.objects.get(user = request.user)
    except Exception,e:  
        return render_with_type(request,'{name}.html'.format(name = link._meta.object_name),{'alert':e})
    if project.status == '待审核':
        if request.method == 'POST':
            form = f(request.POST)
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
                    return render_with_type(request,'Index/{name}Index.html'.format(name = link._meta.object_name),
                            {'projects':rank.objects.filter(status = '待审核'),'alert':'审核成功！','can':True})
                except Exception,e:  
                    error = e
            else:
                error = '请确认是否有审核权限！'
        else:
            form = f()
            return render_with_type(request,'{name}.html'.format(name = link._meta.object_name),{'form':form,'project':project})
    elif auth.isTeacher and auth.ideologyConstruction:
       return render_with_type(request,'Index/{name}Index.html'.format(name = link._meta.object_name),
             {'projects':rank.objects.filter(status = '待审核'),'alert':e,'can':True})
    return render_with_type(request,'Index/{name}Index.html'.format(name = link._meta.object_name),
            {'projects':rank.objects.filter(status = '通过'),'can':False,'alert':error})

def createProject(rank,link,f,request):
    error = None
    try:
            student = Students.objects.get(user = request.user)
            insp = Inspectors.objects.get(number = 10002)
            project = rank.objects.filter(teacher = student)
    except Exception,e:
            error = e
    if not project:
        return render_with_type(request,'Index/{name}Index.html'.format(name = link._meta.object_name),
        {'projects':project,'alert':'您已经创建过项目！','can':False})
    if request.method == 'POST':
        form = f(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = rank(rankName = cd['ProjectName'],
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
                error = e
        else:
            error = '请确认是否已经输入相关信息'
    else:
        form = f()
    return render_with_type(request,'Create/create{name}.html'.format(name = link._meta.object_name),{'form':form,'alert':error})

def JoinProject(rank,link,request,id):
    alert = ''
    try:  
        project = rank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
    except Exception,e:  
        return render_with_type(request,'{name}Detail.html'.format(name = link._meta.object_name),{'alert':e})
    join = link(status = '待审核',StudentNum = student ,rankNum = project , inspector = Inspectors.objects.get(number = 10002))
    join.save()
    alert = '申请成功！'
    return render_with_type(request,'Index/{name}Index.html'.format(name = link._meta.object_name),{'alert':alert})