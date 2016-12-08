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
    StudentNum =models.ForeignKey(Students)
    Score = models.SmallIntegerField()
    totalScore = models.SmallIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

class ResearchProjectRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    rank = models.CharField(max_length = 20)
    role = models.CharField(max_length = 20)
    score = models.SmallIntegerField()
    startingTime = models.DateField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

class ResearchProject(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.PositiveIntegerField()
    ProjectName = models.CharField(max_length = 20)
    ProjectTime = models.DateField()
    SupportText = models.TextField()#支撑文档
    inspectorNum = models.ForeignKey(Inspectors)

class PaperRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    JournalName = models.CharField(max_length = 50)
    Level = models.CharField(max_length = 20)
    AuthorRanking = models.SmallIntegerField()
    score = models.SmallIntegerField()
    startingTime = models.DateField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

class Paper(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.PositiveIntegerField()
    ProjectName = models.CharField(max_length = 20)
    ProjectTime = models.DateField()
    SupportText = models.TextField()#支撑文档 
    inspectorNum = models.ForeignKey(Inspectors)
    
class CompetitionRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    name = models.CharField(max_length = 50)
    Level = models.CharField(max_length = 20)
    rank = models.SmallIntegerField()
    score = models.SmallIntegerField()
    startingTime = models.DateField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

class Competition(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.PositiveIntegerField()
    ProjectTime = models.DateField()
    SupportText = models.TextField()#支撑文档 
    inspectorNum = models.ForeignKey(Inspectors)

class ExchangeRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    type = models.CharField(max_length = 50)
    nature = models.CharField(max_length = 20)
    score = models.SmallIntegerField()
    startingTime = models.DateField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

class Exchange(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.PositiveIntegerField()
    ProjectName = models.CharField(max_length = 20)
    targetName = models.CharField(max_length = 20)
    startTime = models.DateField()
    endTime = models.DateField()
    ProjectContent = models.TextField()
    SupportText = models.TextField()#支撑文档 
    inspectorNum = models.ForeignKey(Inspectors)

class IdeologyConstructionRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    type = models.CharField(max_length = 50)
    name = models.CharField(max_length = 20)
    organizer = models.CharField(max_length = 50)
    startingTime = models.DateField()
    Location = models.CharField(max_length = 50)
    Content = models.TextField()
    score = models.SmallIntegerField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

class IdeologyConstruction(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.PositiveIntegerField()
    SupportText = models.TextField()#支撑文档 
    inspectorNum = models.ForeignKey(Inspectors)

#Lecture
class LectureRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    type = models.CharField(max_length = 50)
    name = models.CharField(max_length = 20)
    organizer = models.CharField(max_length = 50)
    speaker = models.CharField(max_length = 50)
    startingTime = models.DateField()
    Location = models.CharField(max_length = 50)
    Content = models.TextField()
    score = models.SmallIntegerField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

class Lecture(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.PositiveIntegerField()
    SupportText = models.TextField()#支撑文档
    inspectorNum = models.ForeignKey(Inspectors)

#Volunteering
class VolunteeringRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    name = models.CharField(max_length = 20)
    organizer = models.CharField(max_length = 50)
    startingTime = models.DateField()
    Location = models.CharField(max_length = 50)
    volunteerTime = models.PositiveIntegerField()
    Content = models.TextField()
    score = models.SmallIntegerField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

class Volunteering(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.PositiveIntegerField()
    SupportText = models.TextField()#支撑文档
    inspectorNum = models.ForeignKey(Inspectors)

#SchoolActivity
class SchoolActivityRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    type = models.CharField(max_length = 50)
    name = models.CharField(max_length = 20)
    sponsor = models.CharField(max_length = 50)
    organizer = models.CharField(max_length = 50)
    startingTime = models.DateField()
    awardLevel = models.CharField(max_length = 50)
    score = models.SmallIntegerField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

class SchoolActivity(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.PositiveIntegerField()
    SupportText = models.TextField()#支撑文档
    inspectorNum = models.ForeignKey(Inspectors)

#Internship
class InternshipRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    type = models.CharField(max_length = 50)
    startingTime = models.DateField()
    score = models.SmallIntegerField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

class Internship(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.PositiveIntegerField()
    name = models.CharField(max_length = 20)
    startingTime = models.DateField()
    location = models.CharField(max_length = 50)
    job = models.CharField(max_length = 50)
    contribution = models.TextField()
    report = models.TextField()
    appraisal = models.TextField()
    SupportText = models.TextField()#支撑文档
    score = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

class StudentCadreRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    organizitionType = models.CharField(max_length = 50)
    organizitionName = models.CharField(max_length = 20)
    name = models.CharField(max_length = 20)
    score = models.SmallIntegerField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

class StudentCadre(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.PositiveIntegerField()
    startTime = models.DateField()
    endTime = models.DateField()
    opinions = models.TextField()
    SupportText = models.TextField()#支撑文档
    inspectorNum = models.ForeignKey(Inspectors)