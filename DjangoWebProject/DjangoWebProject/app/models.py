# -*- coding: utf-8 -*-
"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Inspectors(models.Model):
    user = models.OneToOneField(User,unique=True,verbose_name=('审查者'))
    inspectorNum = models.PositiveIntegerField()
    name = models.CharField(max_length = 20)

    def __unicode__(self):
        return self.name

class Authorizations(models.Model):
    id = models.PositiveIntegerField(primary_key = True)
    isTeacher = models.BooleanField()
    research = models.BooleanField()
    paper = models.BooleanField()    
    competition = models.BooleanField()
    exchange = models.BooleanField()
    ideologyConstruction = models.BooleanField()
    lecture = models.BooleanField()
    volunteering = models.BooleanField()
    schoolActivity = models.BooleanField()
    internship = models.BooleanField()
    studentCadre = models.BooleanField()

    def __unicode__(self):
        return str(self.id)

class Students(models.Model):
    user = models.OneToOneField(User,unique=True,verbose_name=('用户'))
    auth = models.OneToOneField(Authorizations)
    StudentNum =models.PositiveIntegerField(primary_key = True)
    name = models.CharField(max_length = 20)
    sex =models.BooleanField()#初始值
    year = models.PositiveSmallIntegerField()
    phone = models.BigIntegerField()
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

    def __unicode__(self):
        return str(self.StudentNum)

'''
class Major(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    majorName = models.CharField(max_length = 20)
    inspectorNum = models.ForeignKey(Inspectors)

class StudentMajor(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    majorNum = models.ForeignKey(Major)
    studentNum = models.ForeignKey(Students)
    startTime = models.DateField()
    inspectorNum = models.ForeignKey(Inspectors)

class TrainingProject(models.Model):
    ProjectNum = models.SmallIntegerField(primary_key = True)
    ProjectName = models.CharField(max_length = 20)
    year = models.PositiveSmallIntegerField()    
    classTotalNum = models.PositiveIntegerField()
    classNum = models.PositiveIntegerField()
    classSort = models.PositiveIntegerField()
    inspectorNum = models.PositiveIntegerField()

class Completeness(models.Model):
    number = models.PositiveIntegerField(primary_key = True)
    explain = models.CharField(max_length = 200)

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
    rankNum = models.PositiveIntegerField(primary_key = True)
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
    inspectorNum = models.ForeignKey(Inspectors)'''

#ResearchProject
class ResearchProjectRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    rankName = models.CharField(max_length = 20)
    rank = models.CharField(max_length = 20)
    role = models.CharField(max_length = 20)
    score = models.SmallIntegerField()
    startingTime = models.DateField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return self.rankName

class ResearchProject(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(ResearchProjectRank)
    ProjectName = models.CharField(max_length = 20)
    ProjectTime = models.DateField()
    SupportText = models.TextField()#支撑文档
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)

#Paper
class PaperRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    JournalName = models.CharField(max_length = 50)
    Level = models.CharField(max_length = 20)
    AuthorRanking = models.SmallIntegerField()
    score = models.SmallIntegerField()
    startingTime = models.DateField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return self.rankName

class Paper(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(PaperRank)
    ProjectName = models.CharField(max_length = 20)
    ProjectTime = models.DateField()
    SupportText = models.TextField()#支撑文档 
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)
    
#Competition
class CompetitionRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    name = models.CharField(max_length = 50)
    Level = models.CharField(max_length = 20)
    rank = models.SmallIntegerField()
    score = models.SmallIntegerField()
    startingTime = models.DateField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return self.rankName

class Competition(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(CompetitionRank)
    ProjectTime = models.DateField()
    SupportText = models.TextField()#支撑文档 
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)

#Exchange
class ExchangeRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    type = models.CharField(max_length = 50)
    nature = models.CharField(max_length = 20)
    score = models.SmallIntegerField()
    startingTime = models.DateField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return self.rankName

class Exchange(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(ExchangeRank)
    ProjectName = models.CharField(max_length = 20)
    targetName = models.CharField(max_length = 20)
    startTime = models.DateField()
    endTime = models.DateField()
    ProjectContent = models.TextField()
    SupportText = models.TextField()#支撑文档 
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)

#IdeologyConstruction
class IdeologyConstructionRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    type = models.CharField(max_length = 50)
    name = models.CharField(max_length = 20)
    organizer = models.CharField(max_length = 50)
    startingTime = models.DateField()
    Location = models.CharField(max_length = 50)
    Content = models.TextField()
    score = models.SmallIntegerField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return self.rankName

class IdeologyConstruction(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(IdeologyConstructionRank)
    SupportText = models.TextField()#支撑文档 
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)

#Lecture
class LectureRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    type = models.CharField(max_length = 50)
    name = models.CharField(max_length = 20)
    organizer = models.CharField(max_length = 50)
    speaker = models.CharField(max_length = 50)
    startingTime = models.DateField()
    Location = models.CharField(max_length = 50)
    Content = models.TextField()
    score = models.SmallIntegerField()
    CompleteNum = models.PositiveIntegerField()
    teacherNum = models.ForeignKey(Students)
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return self.rankName

class Lecture(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(LectureRank)
    SupportText = models.TextField()#支撑文档
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)

#Volunteering
class VolunteeringRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    name = models.CharField(max_length = 20)
    organizer = models.CharField(max_length = 50)
    startingTime = models.DateField()
    Location = models.CharField(max_length = 50)
    volunteerTime = models.PositiveIntegerField()
    Content = models.TextField()
    score = models.SmallIntegerField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return self.rankName

class Volunteering(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(VolunteeringRank)
    SupportText = models.TextField()#支撑文档
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)

#SchoolActivity
class SchoolActivityRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    type = models.CharField(max_length = 50)
    name = models.CharField(max_length = 20)
    sponsor = models.CharField(max_length = 50)
    organizer = models.CharField(max_length = 50)
    startingTime = models.DateField()
    awardLevel = models.CharField(max_length = 50)
    score = models.SmallIntegerField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return self.rankName

class SchoolActivity(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(SchoolActivityRank)
    SupportText = models.TextField()#支撑文档
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)

#Internship
class InternshipRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    type = models.CharField(max_length = 50)
    startingTime = models.DateField()
    score = models.SmallIntegerField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return self.rankName 

class Internship(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(InternshipRank)
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
    
    def __unicode__(self):
        return str(self.StudentNum)

class StudentCadreRank(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    organizitionType = models.CharField(max_length = 50)
    organizitionName = models.CharField(max_length = 20)
    name = models.CharField(max_length = 20)
    score = models.SmallIntegerField()
    CompleteNum = models.PositiveIntegerField()
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return self.rankName #返回分级编号

class StudentCadre(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    status = models.PositiveSmallIntegerField(default = 1)
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(StudentCadreRank)
    startTime = models.DateField()
    endTime = models.DateField()
    opinions = models.TextField()
    SupportText = models.TextField()#支撑文档
    inspectorNum = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)