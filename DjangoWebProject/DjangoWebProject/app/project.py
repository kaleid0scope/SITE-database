# -*- coding: utf-8 -*-

from app.forms import *
from app.models import *
from app.parameter import *
from app.Info import *
from app.deco import *
from app.project import *
from django.shortcuts import *
from django.contrib.auth.models import User
from DjangoWebProject import settings
from django.http import HttpRequest
from django.template import RequestContext
from app.create import *
from django.template.loader import get_template
from django.contrib.auth.decorators import * 
from __builtin__ import *
from django.contrib.auth.decorators import * 
from app.views import home

def Error(request,alert = None,template_name = None):
    assert isinstance(request, HttpRequest)
    if template_name == None:
        template_name = 'app/index.html'
    return Ralert(alert)(render)(request,template_name,{'error':True})

#创建
def ProjectCreate(request,rankname):
    if request.method == 'POST':
        project = getView(rankname)(request)
        project.save()
    else:
        form = getForm(rankname)
    return render(request,'create.html',{'form':form})

def InstructorCreate(request,rankname,student):
    
#创建
@authenticated_required
def LinkCreate(request,rankname = None,rankid = None,project = None,student = None,from_url = None):
   #try:
    if project == None and rankid != None and rankname != None:
        rank = getModel(rankname)
        project = rank.objects.get(pk = rankid)
    elif rankid == None and rankname == None :return Error(request,'缺少参数')#get project
    type = getType(request)
    if type == '教师端':
        if student == None: return Error(request,'请指定学生')
        instructor = Instructor.objects.get(user = request.user)
        majors = Major.objects.filter(instructor = instructor).filter(pk = student.major.pk)
        if not majors: return Error(request,'您无权访问')
    elif type == '管理员':
        if student == None: return Error(request,'请指定学生')
    elif type == '学生端':
        student = Students.objects.get(user = request.user)
    else: return Error(request,'您无权访问')
    link = RankLinks(student = student,rtype = project._meta.object_name,rnum = project.pk)
    link.save()
    if from_url == None:
        return redirect(Palert('创建成功')(ProjectIndex)(request,rankname if rankname else None))
    else: return refresh(request,from_url,'创建成功')
   #except Exception,e:
   #         error = e

#删除
@permission_required('auth.is_superuser')
def ProjectDelete(request,linkid):
    #try:
        link = RankLinks.objects.get(pk = int(linkid))
        rank = getModel(link.rtype)
        project = rank.objects.get(id = link.rnum)
        link.delete()
        projectlinks = RankLinks.objects.filter(rnum = project.id)
        if not projectlinks:project.delete()
    #except Exception,e: 
    #    alert = e
        return ProjectIndex(rank,link,request,'已删除' if not e else e)

#详情
@authenticated_required
def ProjectDetail(request,linkid):
    #try:
        link = RankLinks.objects.get(pk = int(linkid))
        rank = getModel(link.rtype)
        project = rank.objects.get(id = link.rnum)

        PV = project.values()
        fields = rank._meta.fields
        FieldProject = {}
        for field in fields : FieldProject[field.verbose_name] = getattr(project,field.name) #该项目键值对

        projectlinks = RankLinks.objects.filter(rnum = project.id)
        members = []
        for link in projectlinks: members.append(link.student) #所有已加入的成员

        type = getType(request)
        if type == '学生端':
            if not link.student == Students.objects.get(user = request.user):
                assert isinstance(request, HttpRequest)
                return Ralert('您只能查看您自己的项目')(render)(request,'app/index.html',{})
            assert isinstance(request, HttpRequest)
            return render(request,'Detail.html',{'project':project,'link':link,'FPS':FieldProject,'FPV':PV,'members':members})
        elif type == '教师端':
            instructor = Instructor.objects.get(user = request.user)
            return render(request,'Detail.html',
            {'project':project,'FPS':FieldProject,'hasJoin':True,'members':members,'manage':False})
        elif type == '管理员':
            dosometing
        if link.objects.filter(rankNum = project).filter(status = '待审核').filter(StudentNum = student):
            tryJoin = True  
        else: tryJoin = False
        return render(request,'Detail.html',{'project':project,'FPS':FieldProject,'members':members,'manage':False,'hasJoin':False,'tryJoin':tryJoin})
    #except Exception,e:
    #    assert isinstance(request, HttpRequest)
    #    return render(request,'app/login.html',{'alert':e})
#列表

@authenticated_required
def ProjectIndex(request,rankname = None):
    #try:
        if rankname != None: rank = getModel(rankname)
        type = getType(request)
        if type == '学生端':
            student = Students.objects.get(user = request.user)
            if rankname != None: links = RankLinks.objects.filter(student = student,rtype = rankname)#所有涉及的项目
            else : links = RankLinks.objects.filter(student = student)
            linksDic,linksP,linksDS,linksNP = {}
            for link in links:
                rank = getModel(link.rtype)
                project = rank.objects.get(pk = link.rnum)
                if link.status == '待审核':
                    linksDS[project.rankName] = value
                elif link.status == '通过':
                    linksP[project.rankName] = value
                else:
                    linksNP[project.rankName] = value
            assert isinstance(request, HttpRequest)
            return render(request,'List.html',
            {'linksP':linksP,
            'linksDS':linksDS,
            'linksNP':linksNP})
        elif type == '教师端':
            instructor = Instructor.objects.get(user = request.user)
            majors = Major.objects.filter(instructor = instructor)
            students = Students.obejects.filter(major__in = majors)
            if rankname != None: links = RankLinks.objects.filter(student__in = students,rtype = rankname)#所有涉及的项目
            else : links = RankLinks.objects.filter(student__in = students)
            linksP = links.filter(status = '通过') 
            linksDS = links.filter(status = '待审核') 
            linksNP = links.filter(status = '未通过') 
            assert isinstance(request, HttpRequest)
            return render(request,'List.html',
            {'linksP':linksP,
            'linksDS':linksDS,
            'linksNP':linksNP})
        elif type == '管理员':
            if rankname != None: links = RankLinks.objects.filter(rtype = rankname)#所有涉及的项目
            else : links = RankLinks.objects.all()
            linksP = links.filter(status = '通过') 
            linksDS = links.filter(status = '待审核') 
            linksNP = links.filter(status = '未通过') 
            assert isinstance(request, HttpRequest)
            return render(request,'List.html',
            {'linksP':linksP,
            'linksDS':linksDS,
            'linksNP':linksNP})
'''except Exception,e:
        assert isinstance(request, HttpRequest)
        return render(request,'app/login.html',{'alert':e})'''
#审核
@teacher_required
def ProjectCheck(request,linkid,rankname = None):
    #try: 
        link = RankLinks.objects.get(pk = int(linkid))
        rank = getModel(link.rtype)
        project = rank.objects.get(pk = link.rnum)
        if fromRank == True:
            name = link.rtype
        elif isinstance(fromRank, basestring):
            name = rankname
        fields = rank._meta.fields
        FieldProject = {}
        for field in fields :
            FieldProject[field.verbose_name] = getattr(project,field.name)#该项目键值对
    #except Exception,e:  
    #    assert isinstance(request, HttpRequest)
    #    return render(request,'app/login.html',{'alert':e})
        if request.method == 'POST':
            form = f(request.POST)
            if form.is_valid():
                    cd = form.cleaned_data
                #try:
                    choice = Choices.objects.get(id = cd['level'])
                    link.complete = choice.complete
                    if request.POST.has_key('passyes'):
                        link.status = '通过'
                        project.active = True
                        project.save()
                    elif request.POST.has_key('passno'):
                        link.status = '未通过'
                    link.save()
                    return redirect(Palert(ProjectIndex)(request,name))
                #except Exception,e:  
                #    error = e
            else:
                error = '请确认是否有审核权限！'
        else:
            form = getForm(link.rtype)
            return render(request,'Pcheck.html',{'form':form,'link':link,'FPS':FieldProject})

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



