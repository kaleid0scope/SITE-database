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
from __builtin__ import getattr


#创建
def ProjectCreate(rank,link,f,request):
    error = None
    try:
            student = Students.objects.get(user = request.user)
            project = rank.objects.filter(teacher = student)
    except Exception,e:
            error = e
    if request.method == 'POST':
        form = f(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = rank(teacher = student,
                                status = '待审核',)
                for field in form:
                    name = field.label
                    project.name = field.value
                project.save()
                return render_with_type(link,request,'first.html',{'alert':'okkkk!'})
            except Exception,e:
                error = e
        else:
            error = '请确认是否已经输入相关信息'
    else:
        form = f()
    return render_with_type(link,request,'Create/create{name}.html'.format(name = link._meta.object_name),{'form':form,'alert':error})
#删除
def ProjectDelete(rank,link,request,id):
    try:
        student = Students.objects.get(user = request.user)
        project = rank.objects.get(id = id)
        links = link.objects.filter(rankNum = project)
    except Exception,e: 
        alert = e
    if project.teacher == student:
        project.delete()
        links.delete()
        return ProjectIndex(rank,link,request,'已删除' if not e else e)
#详情
def ProjectDetail(rank,link,request,id,alert):
    try:  
        project = rank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
        fields = rank._meta.fields
        FieldProject = {}
        for field in fields :
            FieldProject[field.verbose_name] = getattr(project,field.name) #该项目键值对
        links = link.objects.filter(rankNum = project).filter(status = '通过') #已加入的关系
        joins = link.objects.filter(rankNum = project).filter(status = '待审核') #待审核的关系
        members = []
        for link in links:
            members.append(link.StudentNum) #所有已加入的成员
        members.insert(0,project.teacher)
    except Exception,e: 
        return render_with_type(link,request,'Detail.html',{'alert':alert if alert else e})
    if project.teacher == student: #如果为项目的管理者
        e = None
        if request.method == 'POST':
            try:
                num = request.GET.get('num','')
                joiner = Students.objects.get(StudentNum = num)
                joinlink = link.objects.filter(rankNum = project).get(StudentNum = joiner)
            except Exception,e: 
                return render_with_type(link,request,'Detail.html',{'alert':e})
            if request.POST.has_key('passyes'):
                joinlink.status = '通过'
            elif request.POST.has_key('passno'):
                joinlink.status = '未通过'
            joinlink.save()
            e = '审核成功！' 
        return render_with_type(link,request,'Detail.html',
            {'project':project,'FPS':FieldProject,'hasJoin':True,'members':members,'manage':True,'joiners':joins,'alert':alert if alert else e})
    elif members.count(student) == 1: #如果为该项目已通过的成员
        return render_with_type(link,request,'Detail.html',
        {'project':project,'FPS':FieldProject,'hasJoin':True,'members':members})
    tryJoin = True if link.objects.filter(rankNum = project).filter(status = '待审核').filter(StudentNum = student) else False
    return render_with_type(link,request,'Detail.html',{'project':project,'FPS':FieldProject,'members':members,'hasJoin':False,'tryJoin':tryJoin})
#列表
def ProjectIndex(rank,link,request,alert):
    try:  
        student = Students.objects.get(user = request.user)
        linksP = link.objects.filter(StudentNum = student).filter(status = '通过') #所有加入的项目
        links = link.objects.filter(StudentNum = student).filter(status = '待审核') 
        linksNP = link.objects.filter(StudentNum = student).filter(status = '未通过') 
        RawProject = rank.objects.filter(status = '通过').exclude(teacher = student)
        project = []
        for raw in RawProject: 
            if not link.objects.filter(StudentNum = student).filter(rankNum = raw): project.append(raw)
        created = rank.objects.filter(teacher = student)
        joined,join,joinNP = [],[],[]
        for link in linksP: joined.append(link.rankNum)
        for link in links: join.append(link.rankNum)
        for link in linksNP: joinNP.append(link.rankNum)
    except Exception,e: 
        return render_with_type(link,request,'app/login.html',{'alert':alert if alert else e})
    if student.auth.isTeacher and student.auth.ideologyConstruction: #如果是教师，返回待审核的项目
        return render_with_type(link,request,'List.html',
            {'projects':rank.objects.filter(status = '待审核'),'can':True})
    else :  #否则，返回各类项目
        return render_with_type(link,request,'List.html',
            {'projects':project,
            'Cprojects':created, #创建的
            'JprojectsP':joined, #已成功加入
            'Jprojects':join,    #申请加入的
            'JprojectsNP':joinNP,#申请未通过
            'can':False,
            'alert':alert})
#审核
def ProjectCheck(rank,link,f,request,id):
    error = None
    try:  
        project = rank.objects.get(id = int(id))
        auth = Students.objects.get(user = request.user).auth
        fields = rank._meta.fields
        FieldProject = {}
        for field in fields :
            FieldProject[field.verbose_name] = getattr(project,field.name)#该项目键值对
    except Exception,e:  
        return render_with_type(link,request,'Pcheck.html',{'alert':e})
    if project.status == '待审核':
        if request.method == 'POST':
            form = f(request.POST)
            if form.is_valid() and auth.isTeacher:
                cd = form.cleaned_data
                try:
                    choice = Choices.objects.get(id = cd['level'])
                    project.score = choice.score
                    project.complete = choice.complete
                    if request.POST.has_key('passyes'):
                        project.status = '通过'
                    elif request.POST.has_key('passno'):
                        project.status = '未通过'
                    project.save()
                    return render_with_type(link,request,'List.html',
                            {'projects':rank.objects.filter(status = '待审核'),'alert':'审核成功！','can':True})
                except Exception,e:  
                    error = e
            else:
                error = '请确认是否有审核权限！'
        else:
            form = f()
            return render_with_type(link,request,'Pcheck.html'.format(name = link._meta.object_name),{'form':form,'project':project,'FPS':FieldProject})
    elif auth.isTeacher:
       return render_with_type(link,request,'List.html',
             {'projects':rank.objects.filter(status = '待审核'),'alert':e,'can':True})
    return render_with_type(link,request,'List.html',
            {'projects':rank.objects.filter(status = '通过'),'can':False,'alert':error})
#申请加入
def ProjectJoin(rank,link,request,id):
    alert = ''
    try:  
        project = rank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
    except Exception,e:  
        return render_with_type(link,request,'Detail.html',{'alert':e})
    join = link(status = '待审核',StudentNum = student ,rankNum = project)
    join.save()
    alert = '申请成功！'
    return ProjectIndex(rank,link,request,alert)
#手动加入
def ProjectAdd(rank,link,request,id,sid):
    alert = None
    owner = Students.objects.get(user = request.user)
    project = rank.objects.get(id = id)
    student = Students.objects.get(StudentNum = sid)
    links = link.objects.filter(rankNum = project).filter(StudentNum = student).filter(status = '通过')
    Jlinks = link.objects.filter(rankNum = project).filter(StudentNum = student).filter(status = '待审核')
    if not project: alert = '请确认您是否已创建思建活动！'
    elif links or owner == student: alert = '该成员已在项目中！'
    elif Jlinks: 
        join = Jlinks[0]
        join.status = '通过'
        join.save()
    else:
        join = link(status = '通过',StudentNum = student ,rankNum = project)
        join.save()
        alert = '成功添加!'
    return ProjectDetail(IdeologyConstructionRank,IdeologyConstruction,request,id,alert)



