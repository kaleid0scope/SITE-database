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
from app.views import *

def Error(request,alert = None,template_name = None):
    assert isinstance(request, HttpRequest)
    if template_name == None:
        template_name = 'app/project/paper.html'
    return {'error':alert}
    #return Ralert(alert)(render)(request,template_name,{'error':True})

def Success(request,success=None):
    return {'success':success}



def ProjectManage(request,rankname,student = None):
    html = getUrl(rankname)
    result={}
    if request.method == 'POST':#提交的部分
        result= ProjectManagePost(request,rankname,student)
    #获取的部分
    linkDict = ProjectManageGetList(request,rankname,student)
    createform = getForm(rankname)()
    if result:
        linkDict.update(result)
    assert isinstance(request, HttpRequest)#为什么不提前检验它是HttpRequest?
    return render(request,html,dict(linkDict,**{'createForm':createform}))#所有需要的放到模板里去

def ProjectManagePost(request,rankname,student = None):
    html = getUrl(rankname)
    if getType(request) == '学生端':
        project = getView(rankname)(request)
        student = Students.objects.filter(user = request.user)
    else:
        if student == None: 
            #return Error(request,u'缺少参数')
            student = Students.objects.get(StudentNum=201602063)#それは僕！
        if getType(request) == '管理员':
            project = getView(rankname)(request)
        if getType(request) == '辅导员':
            instructor = Instructor.objects.get(user = request.user)
            if not Major.objects.filter(instructor = instructor).filter(pk = student.major.pk): 
                return Error(request,u'您无权访问')
            project = getView(rankname)(request,student)
    if not project: 
        return {'alert':u'表格信息有错误，请确认完整填写'}
    if getModel(rankname).objects.filter(rankName = project.rankName): 
        return {'alert':u'已有相同名称活动！'}
    project.save()
    return LinkAdd(request,project = project,student = student)

def ProjectManageGetList(request,rankname,studentid = None,student = None):
    html = getUrl(rankname)
    if rankname != None: 
        rank = getModel(rankname)
        type = getType(request)
        if type == '学生端':
            student = Students.objects.get(user = request.user)
            if rankname != None: links = RankLinks.objects.filter(student = student,rtype = rankname)#所有涉及的项目
            else : links = RankLinks.objects.filter(student = student)
        elif type == '辅导员':
            instructor = Instructor.objects.get(user = request.user)
            majors = Major.objects.filter(instructor = instructor)
            students = Students.objects.filter(major__in = majors)
            if studentid != None:
                if students.filter(pk = studentid):students = students.filter(pk = studentid)
                else :return Error(request,u'学生不存在或权限验证未通过')
            if rankname != None: links = RankLinks.objects.filter(student__in = students,rtype = rankname)#所有涉及的项目
            else : links = RankLinks.objects.filter(student__in = students)
        elif type == '管理员':
            if studentid != None:
                student = Students.objects.filter(pk = studentid)
                if rankname != None: links = RankLinks.objects.filter(rtype = rankname,student = student)#所有涉及的项目
                else : links = RankLinks.objects.filter(student = student)
            else:
                if rankname != None: links = RankLinks.objects.filter(rtype = rankname)#所有涉及的项目
                else : links = RankLinks.objects.all()
        linksP,linksDS,linksNP = [],[],[]
        for link in links:
                rank = getModel(link.rtype)
                project = rank.objects.get(pk = link.rnum)
                if link.status == '待审核':
                    linksDS.append(ViewLink(n = getVerboseName(link.rtype),rn = project.rankName,l = project))
                elif link.status == '通过':
                    linksP.append(ViewLink(n = getVerboseName(link.rtype),rn = project.rankName,l = project))
                else:
                    linksNP.append(ViewLink(n = getVerboseName(link.rtype),rn = project.rankName,l = project))
        assert isinstance(request, HttpRequest)
        return {'linksP':linksP,'linksDS':linksDS,'linksNP':linksNP}
    #拿到所有的list，已经把里面的类型改成project（XXRank）了

'''管理员访问时带student参数,学生访问时不带
'''
@authenticated_required
def ProjectCreate(request,rankname,student = None):
    if request.method == 'POST':
        if getType(request) == '学生端':
            project = getView(rankname)(request)
            student = Students.objects.filter(user = request.user)
        else:
            if student == None: return Error(request,u'缺少参数')
            if getType(request) == '管理员':project = getView(rankname)(request)
            if getType(request) == '辅导员':
                instructor = Instructor.objects.get(user = request.user)
                if not Major.objects.filter(instructor = instructor).filter(pk = student.major.pk): return Error(request,u'您无权访问')
                project = getView(rankname)(request,student)
        if not project: return render(request,'Pcreate.html',{'alert':u'表格信息有错误'})
        if getModel(rankname).objects.filter(rankName = project.rankName): return render(request,'Pcreate.html',{'alert':u'已有相同名称活动！'})
        project.save()
        return LinkAdd(request,project = project,student = student)
    else:
        form = getForm(rankname)()
    assert isinstance(request, HttpRequest)#为什么不提前检验它是HttpRequest?
    return render(request,'Pcreate.html',{'createForm':form})#空的表

@authenticated_required
def LinkAdd(request,rankname = None,rankid = None,project = None,student = None,from_url = None):
   #try:
    if project == None:
        if rankid != None and rankname != None:
            rank = getModel(rankname)
            project = rank.objects.get(pk = rankid)
        else :return Error(request,u'缺少参数')#get project
    type = getType(request)
    if type == '辅导员':
        if student == None: return Error(request,u'请指定学生')
        instructor = Instructor.objects.get(user = request.user)
        majors = Major.objects.filter(instructor = instructor).filter(pk = student.major.pk)
        if not majors: return Error(request,u'您无权访问')
    elif type == '管理员':
        if student == None: return Error(request,u'请指定学生',template_name=GetUrl(rankname))
    elif type == '学生端':
        student = Students.objects.get(user = request.user)
    else: return Error(request,u'您无权访问')
    link = RankLinks(student = student,rtype = project._meta.object_name,rnum = project.pk,status = '待审核')
    link.save()
    if from_url == None:
        from_url = '/Project/{name}'.format(name = project.__class__.__name__)
    return Success(request,u'创建成功')
   #except Exception,e:
   #         error = e

def ProjectDelete(request,linkid):
        if getType(request) not in ('学生端','辅导员','管理员'):
            return Error(request,u'您无权访问')
    #try:
        link = RankLinks.objects.get(pk = int(linkid))
        rank = getModel(link.rtype)
        project = rank.objects.get(id = link.rnum)
        if getType(request) == '学生端':
            if link.student != Students.objects.get(user = request.user):return Error(request,u'您无权访问')
        if getType(request) == '辅导员':
            instructor = Instructor.objects.get(user = request.user)
            if not Major.objects.filter(instructor = instructor).filter(pk = link.student.major.pk): return Error(request,u'您无权访问')
        link.delete()
        projectlinks = RankLinks.objects.filter(rnum = project.id)
        if not projectlinks:project.delete()#清除空link的project
    #except Exception,e: 
    #    alert = e
        return refresh(request,'/','删除成功')

def ProjectDetail(request,linkid,Valert = None):
    #try:
        if getType(request) not in ('学生端','辅导员','管理员'):
            Error(request,u'您未认证')
        link = RankLinks.objects.get(pk = int(linkid))
        rank = getModel(link.rtype)
        project = rank.objects.get(id = link.rnum)

        fields = rank._meta.fields
        FieldProject = {}
        for field in fields : FieldProject[field.verbose_name] = getattr(project,field.name) #该项目键值对

        projectlinks = RankLinks.objects.filter(rnum = project.id)
        members,majors = [],[]
        for link in projectlinks: 
            members.append(link.student) #所有已加入的成员
            majors.append(link.student.major.pk)
        type = getType(request)
        if type == '学生端':
            if not link.student == Students.objects.get(user = request.user):
                return Ralert('您只能查看您自己的项目')(render)(request,'app/index.html',{})
            manage = True if projectlinks.order_by('id')[0] == link else False
            return render(request,'Detail.html',{'project':project,'link':link,'FPS':FieldProject,'manage':manage,'members':members,'alert':Valert})
        elif type == '辅导员':
            instructor = Instructor.objects.get(user = request.user)
            if not Major.objects.filter(instructor = instructor).filter(pk__in = majors): return Error(request,u'您无权访问')
            return render(request,'Detail.html',{'project':project,'link':link,'FPS':FieldProject,'members':members,'manage':True,'alert':Valert})
        elif type == '管理员':
            return render(request,'Detail.html',{'project':project,'link':link,'FPS':FieldProject,'members':members,'manage':True,'alert':Valert})
    #except Exception,e:
    #    assert isinstance(request, HttpRequest)
    #    return render(request,'app/login.html',{'alert':e})
#列表

class ViewLink(object):
    l = RankLinks
    n = u''
    rn = u''
    def __init__(self, l, n, rn):
        self.l = l
        self.n = n
        self.rn = rn
    pass

def Papers(request):
    form = getForm('Paper')
    return render(request,'app/student/papers.html',{'form':form})

def ProjectIndex(request,rankname = None,studentid = None):
    #try:
        if rankname != None: rank = getModel(rankname)
        type = getType(request)
        if type == '学生端':
            student = Students.objects.get(user = request.user)
            if rankname != None: links = RankLinks.objects.filter(student = student,rtype = rankname)#所有涉及的项目
            else : links = RankLinks.objects.filter(student = student)
        elif type == '辅导员':
            instructor = Instructor.objects.get(user = request.user)
            majors = Major.objects.filter(instructor = instructor)
            students = Students.objects.filter(major__in = majors)
            if studentid != None:
                if students.filter(pk = studentid):students = students.filter(pk = studentid)
                else :return Error(request,u'学生不存在或权限验证未通过')
            if rankname != None: links = RankLinks.objects.filter(student__in = students,rtype = rankname)#所有涉及的项目
            else : links = RankLinks.objects.filter(student__in = students)
        elif type == '管理员':
            if studentid != None:
                student = Students.objects.filter(pk = studentid)
                if rankname != None: links = RankLinks.objects.filter(rtype = rankname,student = student)#所有涉及的项目
                else : links = RankLinks.objects.filter(student = student)
            else:
                if rankname != None: links = RankLinks.objects.filter(rtype = rankname)#所有涉及的项目
                else : links = RankLinks.objects.all()
        linksP,linksDS,linksNP = [],[],[]
        for link in links:
                rank = getModel(link.rtype)
                project = rank.objects.get(pk = link.rnum)
                if link.status == '待审核':
                    linksDS.append(ViewLink(n = getVerboseName(link.rtype),rn = project.rankName,l = link))
                elif link.status == '通过':
                    linksP.append(ViewLink(n = getVerboseName(link.rtype),rn = project.rankName,l = link))
                else:
                    linksNP.append(ViewLink(n = getVerboseName(link.rtype),rn = project.rankName,l = link))
        assert isinstance(request, HttpRequest)
        return render(request,'projects/index.html',
            {'linksP':linksP,
            'linksDS':linksDS,
            'linksNP':linksNP,
            'rankname':rankname,})
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
                    link.choice = choice
                    if request.POST.has_key('passyes'):
                        link.status = '通过'
                        project.active = True
                        project.save()
                        link.save()
                    elif request.POST.has_key('passno'):
                        link.status = '未通过'
                        link.save()
                    return refresh(request,'/Index/{name}'.format(name = project.__class__.__name__),'审核成功')
                #except Exception,e:  
                #    error = e
            else:
                error = '请确认是否有审核权限！'
        else:
            form = ProjectForm()
            return render(request,'Pcheck.html',{'form':form,'link':link,'FPS':FieldProject})

#手动加入
def ProjectAdd(request,linkid,sid):
    link = RankLinks.objects.get(pk = int(linkid))
    rank = getModel(link.rtype)
    project = rank.objects.get(id = link.rnum)
    projectlinks = RankLinks.objects.filter(rnum = project.id)
    if getType(request) == '学生端':
      try:
        if not link.student == Students.objects.get(user = request.user):
            return Ralert('您只能查看您自己的项目')(render)(request,'app/index.html',{})
        student = Students.objects.get(StudentNum = sid)
        if projectlinks.filter(student = student): alert = '该成员已在项目中！'
        join = RankLinks(status = '待审核',student = student ,rtype = link.rtype,rnum = link.rnum)
        join.save()
        alert = '成功添加!'
      except Exception,e:
        alert = '学号对应的学生不存在！'
    if getType(request) == '辅导员' or getType(request) == '管理员':
      try:
        student = Students.objects.get(StudentNum = sid)
        if getType(request) == '辅导员':
            instructor = Instructor.objects.get(user = request.user)
            if not Major.objects.filter(instructor = instructor).filter(pk = student.major.pk):return Error(request,u'您无权访问')
        if projectlinks.filter(student = student): alert = '该成员已在项目中！'
        join = RankLinks(status = '待审核',student = student ,rtype = link.rtype,rnum = link.rnum)
        join.save()
        alert = '成功添加!'
      except Exception,e:
        alert = '学号对应的学生不存在！'
    
    return ProjectDetail(request,linkid,alert)




