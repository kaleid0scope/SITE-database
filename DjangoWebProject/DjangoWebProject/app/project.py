# -*- coding: utf-8 -*-

from app.forms import *
from app.models import *
from app.parameter import *
from app.type import *
from app.Info import *
from app.project import *
from django.shortcuts import *
from django.contrib.auth.models import User
from DjangoWebProject import settings
from django.http import HttpRequest
from django.template import RequestContext
from django.template.loader import get_template
from django.contrib.auth.decorators import * 
from __builtin__ import *


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
def ProjectDelete(request,linkid):
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
def ProjectDetail(request,linkid):
    link = RankLinks.objects.filter(pk = int(linkid))
    rank = getModel(link.rtype)
    project = rank.objects.get(id = link.rnum)

    fields = rank._meta.fields
    FieldProject = {}
    for field in fields :
        FieldProject[field.verbose_name] = getattr(project,field.name) #该项目键值对

    links = link.objects.filter(rankNum = project).filter(status = '通过') #已加入的关系
    joins = link.objects.filter(rankNum = project).filter(status = '待审核') #待审核的关系
    members = []
    for linking in links:
        members.append(linking.StudentNum) #所有已加入的成员
    members.insert(0,project.teacher)
    if project.teacher == student: #如果为项目的管理者
        e = None
        if request.method == 'POST':
            num = request.POST['num']
            joiner = Students.objects.get(StudentNum = int(num))
            joinlink = link.objects.filter(rankNum = project).get(StudentNum = joiner)
            if request.POST.has_key('passyes'):
                joinlink.status = '通过'
            elif request.POST.has_key('passno'):
                joinlink.status = '未通过'
            joinlink.save()
            e = '审核成功！'
            return ProjectDetail(rank,link,request,id,e)
        return render_with_type(link,request,'Detail.html',
            {'project':project,'FPS':FieldProject,'hasJoin':True,'members':members,'manage':True,'joiners':joins,'alert':alert if alert else e})
    elif members.count(student) == 1: #如果为该项目已通过的成员
        return render_with_type(link,request,'Detail.html',
        {'project':project,'FPS':FieldProject,'hasJoin':True,'members':members,'manage':False})
    if link.objects.filter(rankNum = project).filter(status = '待审核').filter(StudentNum = student):
        tryJoin = True  
    else: tryJoin = False
    return render_with_type(link,request,'Detail.html',{'project':project,'FPS':FieldProject,'members':members,'manage':False,'hasJoin':False,'tryJoin':tryJoin})

#列表
@authenticated_required
def ProjectIndex(request,rankname = None):
    try:
        if rankname != None: rank = getModel(rankname)
        type = user_parameter(request).get('type')
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
    except Exception,e:
        assert isinstance(request, HttpRequest)
        return render(request,'app/login.html',{'alert':e})

#审核
@teacher_required
def ProjectCheck(request,linkid,rankname = None):
    try: 
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
    except Exception,e:  
        assert isinstance(request, HttpRequest)
        return render(request,'app/login.html',{'alert':e})
        if request.method == 'POST':
            form = f(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                try:
                    choice = Choices.objects.get(id = cd['level'])
                    link.complete = choice.complete
                    if request.POST.has_key('passyes'):
                        link.status = '通过'
                    elif request.POST.has_key('passno'):
                        link.status = '未通过'
                    link.save()
                    return redirect(Palert(ProjectIndex)(request,name))
                except Exception,e:  
                    error = e
            else:
                error = '请确认是否有审核权限！'
        else:
            form = getForm(link.rtype)
            return render(request,'Pcheck.html',{'form':form,'link':link,'FPS':FieldProject})
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



