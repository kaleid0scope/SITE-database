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
from app.views import *

def Error(request,alert = None,template_name = None):
    assert isinstance(request, HttpRequest)
    if template_name == None:
        template_name = 'app/index.html'
    return Ralert(alert)(render)(request,template_name,{'error':True})


def ProjectCreate(request,rankname,student = None):
    if not Students.objects.filter(user = request.user) or request.user.has_perm('auth.is_instructor'):
            assert isinstance(request, HttpRequest)
            return Ralert('student_required')(render)(request,'app/index.html',{})
    if request.method == 'POST':
        if getType(request) == '学生端':
            project = getView(rankname)(request)
            student = Students.objects.filter(user = request.user)
        else:
            if student == None: return Error(request,u'缺少参数')
            if getType(request) == '管理员':project = getView(rankname,1)(request)
            if getType(request) == '教师端':
                instrutor = Instructor.objects.get(user = request.user)
                if not Major.objects.filter(instructor = instructor).filter(pk = student.major.pk): return Error(request,u'您无权访问')
                project = getView(rankname)(request,student)
        if not project:
            assert isinstance(request, HttpRequest)
            return render(request,'Pcreate.html',{'alert':u'表格信息有错误'})
        project.save()
        return LinkAdd(request,project = project,student = student)
    else:
        form = getForm(rankname)()
    assert isinstance(request, HttpRequest)
    return render(request,'Pcreate.html',{'form':form})

def LinkAdd(request,rankname = None,rankid = None,project = None,student = None,from_url = None):
   #try:
    if not Students.objects.filter(user = request.user) or request.user.has_perm('auth.is_instructor'):
            assert isinstance(request, HttpRequest)
            return Ralert('student_required')(render)(request,'app/index.html',{})
    if project == None and rankid != None and rankname != None:
        rank = getModel(rankname)
        project = rank.objects.get(pk = rankid)
    elif rankid == None and rankname == None :return Error(request,u'缺少参数')#get project
    type = getType(request)
    if type == '教师端':
        if student == None: return Error(request,u'请指定学生')
        instructor = Instructor.objects.get(user = request.user)
        majors = Major.objects.filter(instructor = instructor).filter(pk = student.major.pk)
        if not majors: return Error(request,u'您无权访问')
    elif type == '管理员':
        if student == None: return Error(request,u'请指定学生')
    elif type == '学生端':
        student = Students.objects.get(user = request.user)
    else: return Error(request,u'您无权访问')
    link = RankLinks(student = student,rtype = project._meta.object_name,rnum = project.pk)
    link.save()
    if from_url == None:
        return redirect(Palert(u'创建成功')(ProjectIndex)(request,rankname if rankname else None))
    else: return refresh(request,from_url,u'创建成功')
   #except Exception,e:
   #         error = e

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


def ProjectIndex(request,rankname = None):
    #try:
        if rankname != None: rank = getModel(rankname)
        type = getType(request)
        if type == '学生端':
            student = Students.objects.get(user = request.user)
            if rankname != None: links = RankLinks.objects.filter(student = student,rtype = rankname)#所有涉及的项目
            else : links = RankLinks.objects.filter(student = student)
            linksDic,linksP,linksDS,linksNP = {},{},{},{}
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
            'linksNP':linksNP,
            'rankname':rankname,})
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
            return render(request,'List.html',
            {'linksP':linksP,
            'linksDS':linksDS,
            'linksNP':linksNP})
'''except Exception,e:
        assert isinstance(request, HttpRequest)
        return render(request,'app/login.html',{'alert':e})'''
#审核
def ProjectCheck(request,linkid,rankname = None):
    #try: 
        link = RankLinks.objects.get(pk = int(linkid))
        rank = getModel(link.rtype)
        project = rank.objects.get(pk = link.rnum)
        if not rankname:rankname = link.rtype
        fields = rank._meta.fields
        FieldProject = {}
        for field in fields :
            FieldProject[field.verbose_name] = getattr(project,field.name)#该项目键值对
    #except Exception,e:  
    #    assert isinstance(request, HttpRequest)
    #    return render(request,'app/login.html',{'alert':e})
        if request.method == 'POST':
            form = ProjectForm(request.POST)
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
                    return render(request,'Pcheck.html',{'form':form,'link':link,'FPS':FieldProject})
                #except Exception,e:  
                #    error = e
            else:
                error = '请确认是否有审核权限！'
        else:
            form = ProjectForm()
            return render(request,'Pcheck.html',{'form':form,'link':link,'FPS':FieldProject})



