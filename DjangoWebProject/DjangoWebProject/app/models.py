# -*- coding: utf-8 -*-
"""
Definition of models.
"""

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

statusChoice = (
        ('未通过', '未通过'),
        ('通过', '通过'),
        ('待审核', '待审核'),)

class Complete(models.Model):
    complete1 = models.SmallIntegerField()
    complete2 = models.SmallIntegerField()
    complete3 = models.SmallIntegerField()
    complete4 = models.SmallIntegerField()
    complete5 = models.SmallIntegerField()
    complete6 = models.SmallIntegerField()
    complete7 = models.SmallIntegerField()
    complete8 = models.SmallIntegerField()
    complete9 = models.SmallIntegerField()
    complete10 = models.SmallIntegerField()

class ChoicesTeam(models.Model):
    name = models.CharField(max_length = 50)
    managerScore = models.SmallIntegerField()
    memberScore = models.SmallIntegerField()
    managerComplete = models.SmallIntegerField()
    memberComplete = models.SmallIntegerField()

class Choices(models.Model):
    name = models.CharField(max_length = 50)
    score = models.SmallIntegerField(null = True)
    complete = models.SmallIntegerField()

class Inspectors(models.Model):
    user = models.OneToOneField(User,unique=True,verbose_name=('审查者'))
    number = models.PositiveIntegerField()
    name = models.CharField(max_length = 20)

    def __unicode__(self):
        return self.name

class Authorizations(models.Model):
    id = models.CharField(max_length = 50,primary_key = True)
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
'''
class Complete(models.Model):
    complete1 = models.SmallIntegerField()
    complete2 = models.SmallIntegerField()
    complete3 = models.SmallIntegerField()
    complete4 = models.SmallIntegerField()
    complete5 = models.SmallIntegerField()

class CompleteInformation(models.Model):
    Complete = models.PositiveIntegerField(primary_key = True)
    CompleteExplain = models.TextField()
    majorName = models.CharField(max_length = 20)
    data = models.PositiveIntegerField()

'''

class Students(models.Model):
    user = models.OneToOneField(User,unique=True,verbose_name=('用户'))
    auth = models.OneToOneField(Authorizations)
    StudentNum = models.PositiveIntegerField(primary_key = True)
    rankName = models.CharField(max_length = 20)
    sex = models.BooleanField()#初始值
    year = models.PositiveSmallIntegerField()
    phone = models.BigIntegerField()
    email = models.EmailField()    #特殊符号
    born = models.DateField()
    root = models.CharField(max_length = 50)
    nation = models.CharField(max_length = 50)
    politicalStatus = models.CharField(max_length = 50)
    location = models.CharField(max_length = 50)
    identityType = models.CharField(max_length = 20)
    identityNumber = models.BigIntegerField()
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
    inspector = models.ForeignKey(Inspectors)

class StudentMajor(models.Model):
    ProjectNum = models.PositiveIntegerField(primary_key = True)
    majorNum = models.ForeignKey(Major)
    studentNum = models.ForeignKey(Students)
    startTime = models.DateField()
    inspector = models.ForeignKey(Inspectors)

class TrainingProject(models.Model):
    ProjectNum = models.SmallIntegerField(primary_key = True)
    ProjectName = models.CharField(max_length = 20)
    year = models.PositiveSmallIntegerField()    
    classTotalNum = models.PositiveIntegerField()
    classNum = models.PositiveIntegerField()
    classSort = models.PositiveIntegerField()
    inspector = models.PositiveIntegerField()

class Completeness(models.Model):
    number = models.PositiveIntegerField(primary_key = True)
    explain = models.CharField(max_length = 200)

class TeacherBasis(models.Model):
    TeacherNum = models.PositiveIntegerField(primary_key = True)
    rankName = models.CharField(max_length = 20)
    sex = models.BooleanField()
    phone = models.PositiveIntegerField()
    photo = models.FilePathField()
    email = models.EmailField()
    school = models.CharField(max_length = 50) #学系
    ProfessionalTitle = models.CharField(max_length = 20) #职称
    inspector = models.ForeignKey(Inspectors)
   
class ClassBasis(models.Model):
    rankNum = models.PositiveIntegerField(primary_key = True)
    className = models.CharField(max_length = 20)
    TotalScore = models.PositiveIntegerField()
    TotalTime = models.PositiveIntegerField()
    classIntroduction = models.CharField(max_length = 200)
    classTarget = models.CharField(max_length = 200)    
    classSort = models.CharField(max_length = 50)     #课程类别
    complete = models.PositiveIntegerField(null = True)   #外键
    inspector = models.ForeignKey(Inspectors)

class InClass(models.Model):
    InClassNum = models.PositiveIntegerField(primary_key = True)
    classNum = models.PositiveIntegerField()
    orderNum = models.PositiveIntegerField() #课序号
    term = models.PositiveIntegerField() #开课学期
    room = models.CharField(max_length = 20)  #开课教室
    TeacherNum = models.PositiveIntegerField()
    rankName = models.CharField(max_length = 20)
    inspector = models.ForeignKey(Inspectors)

class ClassScore(models.Model):
    classNum = models.PositiveIntegerField()
    StudentNum =models.ForeignKey(Students)
    Score = models.SmallIntegerField()
    totalScore = models.SmallIntegerField()
    inspector = models.ForeignKey(Inspectors)'''

#ResearchProject
class ResearchProjectRank(models.Model):
    rankName = models.CharField(max_length = 20)
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核')
    rank = models.CharField(max_length = 20)
    ManagerScore = models.SmallIntegerField(null = True)
    MemberScore = models.SmallIntegerField(null = True)
    startingTime = models.DateField()
    teacher = models.ForeignKey(Students)
    ManagerComplete = models.PositiveSmallIntegerField(null = True)
    MemberComplete = models.PositiveSmallIntegerField(null = True)
    inspector = models.ForeignKey(Inspectors)
    SupportText = models.TextField(null = True)#支撑文档

    def __unicode__(self):
        return self.rankName

class ResearchProject(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核')
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(ResearchProjectRank)
    inspector = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)

#Paper-s
class PaperRank(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核')
    rankName = models.CharField(max_length = 50)
    journalName = models.CharField(max_length = 20)
    rank = models.CharField(max_length = 20)
    AuthorRanking = models.SmallIntegerField()
    score = models.SmallIntegerField(null = True)
    startingTime = models.DateField()
    complete = models.PositiveIntegerField(null = True)
    inspector = models.ForeignKey(Inspectors)
    student = models.ForeignKey(Students)
    SupportText = models.TextField(null = True)#支撑文档 

    def __unicode__(self):
        return self.rankName

#Competition-s
class CompetitionRank(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核')
    rankName = models.CharField(max_length = 50)
    Level = models.CharField(max_length = 20)
    rank = models.CharField(max_length = 20)
    score = models.SmallIntegerField(null = True)
    startingTime = models.DateField()
    complete = models.PositiveIntegerField(null = True)
    inspector = models.ForeignKey(Inspectors)
    student = models.ForeignKey(Students)
    SupportText = models.TextField(null = True)#支撑文档 

    def __unicode__(self):
        return self.rankName

#Exchange-s
class ExchangeRank(models.Model):
    rankName = models.CharField(max_length = 50)
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核')
    type = models.CharField(max_length = 50)
    nature = models.CharField(max_length = 20)
    score = models.SmallIntegerField(null = True)
    startTime = models.DateField()
    endTime = models.DateField()
    complete = models.PositiveIntegerField(null = True)
    inspector = models.ForeignKey(Inspectors)
    student = models.ForeignKey(Students)
    SupportText = models.TextField(null = True)#支撑文档 

    def __unicode__(self):
        return self.rankName

#StudentCadre-s
class StudentCadreRank(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核')
    organizitionType = models.CharField(max_length = 50)
    organizitionName = models.CharField(max_length = 20)
    rankName = models.CharField(max_length = 20)
    score = models.SmallIntegerField(null = True)
    complete = models.PositiveIntegerField(null = True)
    inspector = models.ForeignKey(Inspectors)
    student = models.ForeignKey(Students)
    SupportText = models.TextField(null = True)#支撑文档 

    def __unicode__(self):
        return self.rankName 

#IdeologyConstruction
class IdeologyConstructionRank(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核')
    type = models.CharField(max_length = 50)
    rankName = models.CharField(max_length = 20)
    organizer = models.CharField(max_length = 50)
    startingTime = models.DateField()
    Location = models.CharField(max_length = 50)
    Content = models.TextField()
    score = models.SmallIntegerField(null = True)
    complete = models.PositiveIntegerField(null = True)
    inspector = models.ForeignKey(Inspectors)
    teacher = models.ForeignKey(Students)
    SupportText = models.TextField(null = True)#支撑文档 

    def __unicode__(self):
        return self.rankName

class IdeologyConstruction(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核')
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(IdeologyConstructionRank)
    inspector = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)

#Lecture
class LectureRank(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核')
    type = models.CharField(max_length = 50)
    rankName = models.CharField(max_length = 20)
    organizer = models.CharField(max_length = 50)
    speaker = models.CharField(max_length = 50)
    startingTime = models.DateField()
    Location = models.CharField(max_length = 50)
    Content = models.TextField()
    score = models.SmallIntegerField(null = True)
    complete = models.PositiveIntegerField(null = True)
    teacher = models.ForeignKey(Students)
    inspector = models.ForeignKey(Inspectors)
    SupportText = models.TextField(null = True)#支撑文档 

    def __unicode__(self):
        return self.rankName

class Lecture(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核')
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(LectureRank)
    inspector = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)

#Volunteering
class VolunteeringRank(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核')
    rankName = models.CharField(max_length = 20)
    organizer = models.CharField(max_length = 50)
    startingTime = models.DateField()
    Location = models.CharField(max_length = 50)
    volunteerTime = models.PositiveIntegerField()
    Content = models.TextField()
    score = models.SmallIntegerField(null = True)
    complete = models.PositiveIntegerField(null = True)
    inspector = models.ForeignKey(Inspectors)
    teacher = models.ForeignKey(Students)
    SupportText = models.TextField(null = True)#支撑文档 

    def __unicode__(self):
        return self.rankName

class Volunteering(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核')
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(VolunteeringRank)
    inspector = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)

#SchoolActivity
class SchoolActivityRank(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核')
    type = models.CharField(max_length = 50)
    rankName = models.CharField(max_length = 20)
    sponsor = models.CharField(max_length = 50)
    organizer = models.CharField(max_length = 50)
    startingTime = models.DateField()
    awardLevel = models.CharField(max_length = 50)
    score = models.SmallIntegerField(null = True)
    complete = models.PositiveIntegerField(null = True)
    inspector = models.ForeignKey(Inspectors)
    teacher = models.ForeignKey(Students)
    SupportText = models.TextField(null = True)#支撑文档 

    def __unicode__(self):
        return self.rankName

class SchoolActivity(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核')
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(SchoolActivityRank)
    inspector = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)

#Internship
class InternshipRank(models.Model):
    rankName = models.CharField(max_length = 20)
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核')
    type = models.CharField(max_length = 50)
    InternshipTime = models.DateField()
    score = models.SmallIntegerField(null = True)
    complete = models.PositiveIntegerField(null = True)
    inspector = models.ForeignKey(Inspectors)
    teacher = models.ForeignKey(Students)
    SupportText = models.TextField(null = True)#支撑文档 

    def __unicode__(self):
        return self.rankName 

class Internship(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核')
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(InternshipRank)
    rankName = models.CharField(max_length = 20)
    Time = models.DateField()
    location = models.CharField(max_length = 50)
    job = models.CharField(max_length = 50)
    contribution = models.TextField()
    report = models.TextField()
    appraisal = models.TextField()
    score = models.PositiveIntegerField()
    inspector = models.ForeignKey(Inspectors)
    
    def __unicode__(self):
        return str(self.StudentNum)