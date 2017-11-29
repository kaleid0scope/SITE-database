# -*- coding: utf-8 -*-

from django.shortcuts import render
from DjangoWebProject import settings
from django.http import HttpRequest
from django.template import RequestContext
from django.template.loader import get_template
from datetime import datetime
from django.shortcuts import *
from django.contrib.auth.models import User
from app.forms import *
from app.models import *
from app.Info import *
from app.project import *
from django.http import HttpResponse
from django.http import HttpResponseRedirect  
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import * 
import random,time
import MySQLdb
from django.template.context import Context
import sys
from django.core.files.uploadedfile import TemporaryUploadedFile
import os
from deco import *
from app.excel import *
from django.contrib.contenttypes.models import ContentType
import DjangoWebProject.settings

'''  课程学生相关。

               '''

def getls(request,sid = None):
    if sid: st = Students.objects.get(StudentNum = sid)
    if getType(request) == '教师端':
        teacher = Teacher.objects.get(user = request.user)
        lessons = Lesson.objects.filter(teacher = teacher)
        scores = Score.objects.filter(lesson_in = lessons) if not sid else Score.objects.filter(lesson_in = lessons).filter(student = st)
        if sid :
            lessons = []
            for score in scores: lessons.append(score.lesson)
        students = []
        if not sid:
            for score in scores:
                if score.student not in students : students.append(score.student)
        else : students.append(st)
    elif getType(request) == '辅导员':
        instructor = Instructor.objects.get(user = request.user)
        majors = Major.objects.filter(instructor = instructor)
        students = Students.objects.filter(major__in = majors) if not sid else [st]
        scores = Score.objects.filter(student__in = students)
        lessons = []
        for score in scores:
            if score.lesson not in lessons : lessons.append(score.student)
    elif getType(request) == '管理员':
        students = Students.objects.all() if not sid else [st]
        scores = Score.objects.all() if not sid else Score.objects.filter(student = st)
        lessons = Lesson.objects.all()
        if sid :
            lessons = []
            for score in scores: lessons.append(score.lesson)
    elif getType(request) == '学生端':
        students = Students.objects.filter(user = request.user)
        scores = Score.objects.filter(student = students[0])
        lessons = []
        for score in scores: lessons.append(score.lesson)
    else:return Error(request,u'您无权访问')
    return {'lessons':lessons,'students':students,'scores':scores}

#注意scores和projects也是queryset
class SL(object):
    def __init__(self, st, score, rl):
        self.student = st
        self.scores = score
        self.rl = rl
    pass

class rl(object):
    def __init__(self, name , rank, ranklink):
        self.name = name
        self.project = rank
        self.ranklink = ranklink
    pass

def studentList(request):
    students = getls(request)['students']
    sls = []        
    rls = []
    for student in students:
        score = Score.objects.filter(student = student)
        ranklinks = RankLinks.objects.filter(student = student)
        for link in ranklinks:
            rank = getModel(link.rtype)
            project = rank.objects.get(pk = link.rnum)
            rls.append(rl(getVerboseName(link.rtype),project,link))
        sls.append(SL(student,score,rls))
    return render(request,'app/stlist.html',{'list':sls})

class LS(object):
    def __init__(self, ls, score, ct):
        self.lesson = ls
        self.score = score
        self.count = ct
    pass

def lessonList(request,sid = None):
    if sid: student = Students.objects.get(StudentNum = sid)
    lessons = getls(request,sid)['lessons']
    lss = []
    for lesson in lessons:
        score = Score.objects.filter(lesson = lesson)
        lss.append(LS(lesson,score,score.count()))
    return render(request,'app/lessonlist.html',{'list':lss})

def scoreList(request,lid = None,sid = None):
    scores = getls(request,sid)['scores'] if sid else getls(request)['scores']
    #try: st = Students.objects.get(user = request.user)
    #except Exception,e: st = None
    #sti =  Students.objects.get(id = sid) if sid else st
    sc = scores.filter(lesson = Lesson.objects.get(StudentNum = lid)) if lid else scores
    return render(request,'app/scorelist.html',{'list':sc})#,'st': sti})

def readPlan(request):
    if getType(request) not in ('学生端'):
        Error(request,u'学生才能访问')
    plan = Students.objects.get(user = request.user).major.plan
    if plan:
        return HttpResponse(plan.read())
    else:
        return render(request,'app/blank.html',{'message':'培养方案未上传'})