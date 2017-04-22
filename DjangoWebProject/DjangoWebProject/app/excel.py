import uuid
import xlrd
from app.models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from __builtin__ import range
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
          Major     = sheet.cell(r,14).value
          Province       = sheet.cell(r,15).value
          if not User.objects.filter(username = studentNum):
            instructor = Instructor.objects.get(major = Major)
            thecomplete = Complete()
            thecomplete.save()
            theuser = User(username = studentNum ,password = make_password('uibe'+IdentityNumber[-6:]),email = Email)
            theuser.save()
            theauth = Authorizations(isTeacher = False,
                                   research = False,
                                   paper = False,
                                   competition = False,
                                   exchange = False,
                                   ideologyConstruction = False,
                                   lecture = False,
                                   volunteering = False,
                                   schoolActivity = False,
                                   internship = False,
                                   studentCadre = False)
            theauth.save()
            student = Students(user =theuser,
                             auth =theauth, 
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
                             instructor = instructor,
                             major =Major,
                             province =Province,
                             complete = thecomplete,
                             collegeEntranceExaminationScore =CollegeEntranceExaminationScore)
            student.save()
    return True