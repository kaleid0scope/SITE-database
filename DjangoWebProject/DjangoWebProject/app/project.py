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
        links = link.objects.filter(rankNum = project).filter(status = 'ͨ��') #���м������Ŀ�Ĺ�ϵ
        joins = link.objects.filter(rankNum = project).filter(status = '�����') #�����������Ŀ�Ĺ�ϵ
        members = []
        for link in links:
            members.append(link.StudentNum) #���и���Ŀ�ĳ�Ա
        members.insert(0,student)
    except Exception,e: 
        return render_with_type(request,'{name}Detail.html'.format(name = link._meta.object_name),{'alert':e})
    if project.teacher == student: #Ϊ����Ŀ������
        alert = None
        if request.method == 'POST':
            try:
                num = request.GET.get('num','')
                joiner = Students.objects.get(StudentNum = num)
                joinlink = link.objects.filter(rankNum = project).get(StudentNum = joiner)
            except Exception,e: 
                return render_with_type(request,'{name}Detail.html'.format(name = link._meta.object_name),{'alert':e})
            if request.POST.has_key('passyes'):
                joinlink.status = 'ͨ��'
            elif request.POST.has_key('passno'):
                joinlink.status = 'δͨ��'
            joinlink.save()
            alert = '��˳ɹ���' #���ѧ���ļ���
        return render_with_type(request,'{name}Detail.html'.format(name = link._meta.object_name),
            {'project':project,'hasJoin':True,'members':members,'manage':True,'joiners':joins,'alert':alert})
    elif members.count(student) == 1: #��Ŀ�������û�Ϊ��Ա
        return render_with_type(request,'{name}Detail.html'.format(name = link._meta.object_name),{'project':project,'hasJoin':True,'members':members})
    return render_with_type(request,'{name}Detail.html'.format(name = link._meta.object_name),{'project':project})

def ProjectIndex(rank,link,request):
    try:  
        student = Students.objects.get(user = request.user)
        links = link.objects.filter(StudentNum = student) #�漰�����û�����Ŀ��ϵ��
        created = rank.objects.filter(teacher = student)
        joined = []
        for link in links:
            joined.append(link.rankNum)
    except Exception,e: 
        return render_with_type(request,'index.html',{'constructions':link.objects.filter(StudentNum = student),'alert':e})
    if student.auth.isTeacher and student.auth.ideologyConstruction: #��������Ȩ�ޣ���������б�
        return render_with_type(request,'Index/{name}Index.html'.format(name = link._meta.object_name),{'projects':rank.objects.filter(status = '�����'),'can':True})
    else :  #���򷵻��Ѽ���Ϳɼ������Ŀ
        return render_with_type(request,'Index/{name}Index.html'.format(name = link._meta.object_name),
            {'projects':rank.objects.filter(status = 'ͨ��'),
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
    if project.status == 'δͨ��':
        if request.method == 'POST':
            form = f(request.POST)
            if form.is_valid() and auth.isTeacher and auth.ideologyConstruction:
                cd = form.cleaned_data
                try:
                    choice = Choices.objects.get(id = cd['level'])
                    project.score = choice.score
                    project.complete = choice.complete
                    if request.POST.has_key('passyes'):
                        project.status = 'ͨ��'
                    elif request.POST.has_key('passno'):
                        project.status = 'δͨ��'
                    project.inspector = inspector
                    project.save()
                    return render_with_type(request,'Index/{name}Index.html'.format(name = link._meta.object_name),\
                            {'projects':rank.objects.filter(status = '�����'),'alert':'��˳ɹ���','can':True})
                except Exception,e:  
                    error = e
            else:
                error = '�����Ƿ���Ȩ����ˣ�'
        else:
            form = f()
            return render_with_type(request,'{name}.html'.format(name = link._meta.object_name),{'form':form,'project':project})
    elif auth.isTeacher and auth.ideologyConstruction:
       return render_with_type(request,'Index/{name}Index.html'.format(name = link._meta.object_name),
             {'projects':rank.objects.filter(status = '�����'),'alert':'���ʧ�ܣ��û�����!�������{{e}}'.format(e = error),'can':True})
    return render_with_type(request,'Index/{name}Index.html'.format(name = link._meta.object_name),
            {'projects':rank.objects.filter(status = 'ͨ��'),'can':False,'alert':error})

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
        {'projects':project,'alert':'���Ѿ���������Ŀ��','can':False})
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
                                status = '�����',
                                inspector = insp,)
                project.save()
                return render_with_type(request,'first.html',{'alert':'okkkk!'})
            except Exception,e:
                error = e
        else:
            error = '��ȷ���Ƿ�����д�����Ϣ��'
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
    join = link(status = '�����',StudentNum = student ,rankNum = project , inspector = Inspectors.objects.get(number = 10002))
    join.save()
    alert = '�ɹ����룡'
    return render_with_type(request,'Index/{name}Index.html'.format(name = link._meta.object_name),{'alert':alert})