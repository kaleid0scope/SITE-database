# -*- coding: utf-8 -*-
"""
Definition of models.
"""

from django.db import models

# Create your models here.

class Inspectors(models.Model):
    inspectorNum = models.PositiveIntegerField()
    name = models.CharField(max_length = 20)

class Students(models.Model):
    StudentNum =models.PositiveIntegerField('学号',primary_key = True)
    name = models.CharField(max_length = 20)
    sex =models.BooleanField()                         #初始值
    year = models.PositiveSmallIntegerField()
    phone = models.PositiveIntegerField()
    email = models.EmailField()    #特殊符号
    photo = models.FilePathField()
    born = models.DateField()
    root = models.CharField(max_length = 50)
    nation = models.CharField(max_length = 50)
    politicalStatus = models.CharField(max_length = 50)
    location = models.CharField(max_length = 50)
    identityType = models.CharField(max_length = 20)
    identityNumber = models.PositiveIntegerField()
    speciality = models.CharField(max_length = 50)
    province = models.CharField(max_length = 50)
    collegeEntranceExaminationScore = models.PositiveSmallIntegerField()
    inspector = models.ForeignKey(Inspectors)

class Teachers(models.Model):
    TeacherNum = models.PositiveIntegerField(default = 10000 , primary_key = True)
    name = models.CharField(max_length = 20)
    sex =models.BooleanField()

class Projects(models.Model):
    name = models.CharField(max_length = 20)
    number = models.SmallIntegerField(primary_key = True)
    teacher = models.ForeignKey(Teachers)
    Location = models.CharField(max_length = 50)

class Relation(models.Model):
    project = models.ForeignKey(Projects)
    student = models.ForeignKey(Students)

class Majorname(models.Model):
    majorName = models.CharField(max_length = 20)
    number = models.SmallIntegerField(primary_key = True)
    inspectorNum = models.ForeignKey(Inspectors)

class StudentMajor(models.Model):
    StudentNum = models.SmallIntegerField(primary_key = True)
    majorName = models.CharField(max_length = 20)
    inspectorNum = models.PositiveIntegerField()

class TrainingProject(models.Model):
    ProjectNum = models.SmallIntegerField(primary_key = True)
    ProjectName = models.CharField(max_length = 20)
    year = models.PositiveSmallIntegerField()    
    classTotalNum = models.PositiveIntegerField()
    classNum = models.PositiveIntegerField()
    classSort = models.PositiveIntegerField()
    inspectorNum = models.PositiveIntegerField()

class Completeness(models.Model):
    CompleteDataExplain = models.PositiveIntegerField(primary_key = True)
   

class CompleteInformation(models.Model):
    CompleteNum = models.PositiveIntegerField(primary_key = True)
    CompleteExplain = models.TextField()
    majorName = models.CharField(max_length = 20)
    data = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

class TeacherBasis(models.Model):
    TeacherNum = models.PositiveIntegerField(primary_key = True)
    name = models.CharField(max_length = 20)
    sex = models.BooleanField()
    phone = models.PositiveIntegerField()
    photo = models.FilePathField()
    email = models.EmailField()
    school = models.CharField(max_length = 50) #学系
    ProfessionalTitle = models.CharField(max_length = 20) #职称
    inspectorNum = models.ForeignKey(Inspectors)
   
class ClassBasis(models.Model):
    classNum = models.PositiveIntegerField(primary_key = True)
    className = models.CharField(max_length = 20)
    TotalScore = models.PositiveIntegerField()
    TotalTime = models.PositiveIntegerField()
    classIntroduction = models.CharField(max_length = 200)
    classTarget = models.CharField(max_length = 200)    
    classSort = models.CharField(max_length = 50)     #课程类别
    CompleteNum = models.PositiveIntegerField()   #外键
    inspectorNum = models.ForeignKey(Inspectors)

class InClass(models.Model):
    InClassNum = models.PositiveIntegerField(primary_key = True)
    classNum = models.PositiveIntegerField()
    orderNum = models.PositiveIntegerField() #课序号
    term = models.PositiveIntegerField() #开课学期
    room = models.CharField(max_length = 20)  #开课教室
    TeacherNum = models.PositiveIntegerField()
    name = models.CharField(max_length = 20)
    inspectorNum = models.ForeignKey(Inspectors)

class ClassScore(models.Model):
    classNum = models.PositiveIntegerField()
    StudentNum =models.PositiveIntegerField()
    Score = models.SmallIntegerField()
    totalScore = models.SmallIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

class ResearchProjectRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    rank = models.CharField(max_length = 20)
    role = models.CharField(max_length = 20)
    score = models.SmallIntegerField()
    startingTime = models.PositiveIntegerField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

class ResearchProject(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    StudentNum =models.PositiveIntegerField()
    rankNum = models.PositiveIntegerField()
    ProjectName = models.CharField(max_length = 20)
    ProjectTime = models.PositiveIntegerField()  #支撑文档
    inspectorNum = models.ForeignKey(Inspectors)
    