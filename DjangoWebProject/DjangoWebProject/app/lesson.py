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

def getls(request):
    if getType(request) == '教师端':
        teacher = Teacher.objects.get(user = request.user)
        lessons = Lesson.objects.filter(teacher = teacher)
        scores = Score.objects.filter(lesson_in = lessons)
        students = []
        for score in scores:
            if score.student not in students : students.append(score.student)
    elif getType(request) == '辅导员':
        instructor = Instructor.objects.get(user = request.user)
        majors = Major.objects.filter(instructor = instructor)
        students = Students.objects.filter(major__in = majors)
        scores = Score.objects.filter(student__in = students)
        lessons = []
        for score in scores:
            if score.lesson not in lessons : lessons.append(score.student)
    elif getType(request) == '管理员':
        lessons = Lesson.objects.all()
        students = Students.objects.all()
        scores = Score.objects.all()
    else:return Error(request,u'您无权访问')
    return {'lessons':lessons,'students':students,'scores':scores}

#注意scores和projects也是queryset
class SL(object):
    def __init__(self, st, score, rl ,ct):
        self.student = st
        self.scores = score
        self.projects = rl
    pass

def studentList(request):
    students = getls(request)['students']
    sls = []
    for student in students:
        score = Score.objects.filter(student = student)
        ranklinks = RankLinks.projects.filter(student = student)
        sls.append(SL(student,score,ranklinks))
    return render(request,'app/stlist.html',{'list':sls})

class LS(object):
    def __init__(self, st, score, ct):
        self.student = st
        self.score = score
        self.count = ct
    pass

def lessonList(request):
    lessons = getls(request)['lessons']
    lss = []
    for lesson in lessons:
        score = Score.objects.filter(lesson = lesson)
        lss.append(SL(lesson,score,score.count()))
    return render(request,'app/stlist.html',{'list':lss})