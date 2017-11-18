# -*- coding: utf-8 -*-

import uuid
import xlrd
from app.models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from __builtin__ import range
from app.Info import *
import os
import random,time
from datetime import datetime

def ExcelRegister(path):
    book = xlrd.open_workbook(path)
    sheet = book.sheets()[0]  
    for r in range(1, sheet.nrows):
          CollegeEntranceExaminationScore  = str(int(sheet.cell(r,0).value))
          studentNum     = str(int(sheet.cell(r,1).value))
          Name           = sheet.cell(r,2).value
          Sex            = str(int(sheet.cell(r,3).value))
          Year           = str(int(sheet.cell(r,4).value))
          Phone          = str(int(sheet.cell(r,5).value))
          Email          = sheet.cell(r,6).value
          Born           = sheet.cell(r,7).value
          Root           = sheet.cell(r,8).value
          Nation         = sheet.cell(r,9).value
          PoliticalStatus= sheet.cell(r,10).value
          Location       = sheet.cell(r,11).value
          IdentityType   = sheet.cell(r,12).value
          IdentityNumber = str(int(sheet.cell(r,13).value))
          MajorName     = sheet.cell(r,14).value
          Province       = sheet.cell(r,15).value
          if True : #not User.objects.filter(username = studentNum):
            thecomplete = Complete()
            thecomplete.save()
            theuser = User(username = studentNum ,password = make_password('uibe'+IdentityNumber[-6:]),email = Email)
            theuser.save()
            Inst = Instructor.objects.get_or_create(name = '未知辅导员',num = 1,user = User.objects.get(username = 'sea'))[0]
            if not type(Inst) == Instructor: 
                inst = Inst[0]
                inst.save()
            else:inst = Inst
            major = Major.objects.get_or_create(name = MajorName,instructor = Inst)
            if not type(major) == Major:
                mj = major[0]
                mj.save()
            else:mj = major
            student = Students(user =theuser,
                             StudentNum =int(studentNum), 
                             rankName =Name, 
                             sex =int(Sex), 
                             year =int(Year), 
                             phone = int(Phone),
                             email = Email,
                             born = datetime.strptime(Born,'%Y-%m-%d'),
                             root =Root,
                             nation =Nation,
                             politicalStatus =PoliticalStatus,
                             location =Location,
                             identityType =IdentityType,
                             identityNumber =int(IdentityNumber),
                             major = mj,
                             province =Province,
                             complete = thecomplete,
                             collegeEntranceExaminationScore =CollegeEntranceExaminationScore)
            student.save()
    return True

def ExcelImportLesson(path):
    book = xlrd.open_workbook(path)
    sheet = book.sheets()[0]  
    for r in range(1, sheet.nrows):
          Name           = sheet.cell(r,0).value            #课程名称
          Num            = sheet.cell(r,1).value            #课序号
          Credit         = str(int(sheet.cell(r,2).value))  #学分
          Time           = str(int(sheet.cell(r,3).value))  #学时
          Introduction   = sheet.cell(r,4).value            #课程介绍
          ClassTarget    = sheet.cell(r,5).value            #课程目标
          ClassSort      = sheet.cell(r,6).value            #课程类别
          lesson = Lesson(name = Name,num = Num,credit = Credit,time = Time,introduction = Introduction,classSort = ClassSort,classTarget = ClassTarget)
          lesson.save()
    return True

def ExcelImportLink(path,project):
    book = xlrd.open_workbook(path)
    sheet = book.sheets()[0]  
    for r in range(1, sheet.nrows):
          num           = sheet.cell(r,0).value         #学生学号

          link = RankLinks.objects.get(pk = linkid)
          student = Students.objects.get(pk = num)
          newlink = RankLinks(student = student,rtype= link.rtype,rum = link.rnum,status = '通过')
          newlink.save()
    return True