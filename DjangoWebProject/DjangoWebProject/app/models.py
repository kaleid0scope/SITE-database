# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.

statusChoice = (
        ('未通过', '未通过'),
        ('通过', '通过'),
        ('待审核', '待审核'),)


class CompleteInformation(models.Model):
    Complete = models.PositiveIntegerField(primary_key = True,verbose_name ='学术竞赛' )
    CompleteExplain = models.TextField(verbose_name ='学术竞赛简介' )

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
    name = models.CharField(max_length = 50,verbose_name ='队伍名称' )
    managerScore = models.SmallIntegerField(verbose_name ='队长分数' )
    memberScore = models.SmallIntegerField(verbose_name ='队员分数' )
    managerComplete = models.SmallIntegerField(verbose_name ='队长完成度' )
    memberComplete = models.SmallIntegerField(verbose_name ='队员完成度' )

class Choices(models.Model):
    name = models.CharField(max_length = 50,verbose_name ='队伍名称')
    score = models.SmallIntegerField(null = True,blank = True,verbose_name ='分数')
    complete = models.SmallIntegerField(verbose_name ='完成度')

class Inspectors(models.Model):
    user = models.OneToOneField(User,unique=True,verbose_name=('审查者'))
    number = models.PositiveIntegerField(verbose_name ='审查者编号' )
    name = models.CharField(max_length = 20,verbose_name ='审核者名称')

    def __unicode__(self):
        return self.name

class Authorizations(models.Model):
    id = models.CharField(max_length = 50,primary_key = True,verbose_name ='id' )
    isTeacher = models.BooleanField(verbose_name ='教师权限' )
    research = models.BooleanField(verbose_name ='科研立项权限' )
    paper = models.BooleanField(verbose_name ='学术论文权限' )    
    competition = models.BooleanField(verbose_name ='学术竞赛权限' )
    exchange = models.BooleanField(verbose_name ='交流交换权限' )
    ideologyConstruction = models.BooleanField(verbose_name ='思建活动权限' )
    lecture = models.BooleanField(verbose_name ='讲座活动权限' )
    volunteering = models.BooleanField(verbose_name ='志愿活动权限' )
    schoolActivity = models.BooleanField(verbose_name ='校园活动权限' )
    internship = models.BooleanField(verbose_name ='实践活动权限' )
    studentCadre = models.BooleanField(verbose_name ='学生干部权限' )

    def __unicode__(self):
        return str(self.id)

class Students(models.Model):
    user = models.OneToOneField(User,unique=True,verbose_name=('用户'))
    auth = models.OneToOneField(Authorizations,verbose_name ='权限' )
    StudentNum = models.PositiveIntegerField(primary_key = True,verbose_name ='学号' )
    rankName = models.CharField(max_length = 20,verbose_name ='学生姓名' )
    sex = models.BooleanField(verbose_name ='性别' )#初始值
    year = models.PositiveSmallIntegerField(verbose_name ='入学年份' )
    phone = models.BigIntegerField(verbose_name ='手机号码' )
    email = models.EmailField(verbose_name ='电子邮箱' )#待修改
    born = models.DateField(verbose_name ='出生年月' )
    root = models.CharField(max_length = 50,verbose_name ='籍贯')
    nation = models.CharField(max_length = 50,verbose_name ='民族')
    politicalStatus = models.CharField(max_length = 50,verbose_name ='政治面貌')
    location = models.CharField(max_length = 50,verbose_name ='国家地区')
    identityType = models.CharField(max_length = 20,verbose_name ='身份证件类型')
    identityNumber = models.BigIntegerField(verbose_name ='身份证号码')
    speciality = models.CharField(max_length = 50,verbose_name ='专业名称')
    province = models.CharField(max_length = 50,verbose_name ='生源省份')
    collegeEntranceExaminationScore = models.PositiveSmallIntegerField(verbose_name ='高考分数')

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
    complete = models.PositiveIntegerField(null = True,blank = True)   #外键
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
    rankName = models.CharField(max_length = 20,verbose_name ='科研立项名称')
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核',verbose_name ='状态')
    rank = models.CharField(max_length = 20,verbose_name ='科研立项等级')
    ManagerScore = models.SmallIntegerField(null = True,blank = True,verbose_name ='队长分数')
    MemberScore = models.SmallIntegerField(null = True,blank = True,verbose_name ='队员分数')
    startingTime = models.DateField(verbose_name ='开始时间')
    teacher = models.ForeignKey(Students,verbose_name ='指导教师')
    ManagerComplete = models.PositiveSmallIntegerField(null = True,blank = True,verbose_name ='队长完成度')
    MemberComplete = models.PositiveSmallIntegerField(null = True,blank = True,verbose_name ='队员完成度')
    inspector = models.ForeignKey(Inspectors,verbose_name ='审核者')
    SupportText = models.TextField(null = True,blank = True,verbose_name ='支撑文档')#支撑文档

    def __unicode__(self):
        return self.rankName

class ResearchProject(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核',verbose_name ='状态')
    StudentNum =models.ForeignKey(Students,verbose_name ='学号')
    rankNum = models.ForeignKey(ResearchProjectRank)
    inspector = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)

#Paper-s
class PaperRank(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核',verbose_name ='状态')
    rankName = models.CharField(max_length = 50,verbose_name ='论文名称')
    journalName = models.CharField(max_length = 20,verbose_name ='期刊名称')
    rank = models.CharField(max_length = 20,verbose_name ='等级')
    AuthorRanking = models.SmallIntegerField(verbose_name ='作者顺序')
    score = models.SmallIntegerField(null = True,blank = True,verbose_name ='评分')
    startingTime = models.DateField(verbose_name ='开始时间')
    complete = models.PositiveIntegerField(null = True,blank = True,verbose_name ='完成度')
    inspector = models.ForeignKey(Inspectors)
    student = models.ForeignKey(Students)
    SupportText = models.TextField(null = True,blank = True,verbose_name ='支撑文档')#支撑文档 

    def __unicode__(self):
        return self.rankName

#Competition-s
class CompetitionRank(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核',verbose_name ='状态')
    rankName = models.CharField(max_length = 50,verbose_name ='学术竞赛名称')
    Level = models.CharField(max_length = 20,verbose_name ='学术竞赛等级')
    rank = models.CharField(max_length = 20,verbose_name ='学生排名')
    score = models.SmallIntegerField(null = True,blank = True,verbose_name ='分数')
    startingTime = models.DateField(verbose_name ='开始时间')
    complete = models.PositiveIntegerField(null = True,blank = True,verbose_name ='完成度')
    inspector = models.ForeignKey(Inspectors)
    student = models.ForeignKey(Students)
    SupportText = models.TextField(null = True,blank = True,verbose_name ='支撑文档')#支撑文档 

    def __unicode__(self):
        return self.rankName

#Exchange-s
class ExchangeRank(models.Model):
    rankName = models.CharField(max_length = 50,verbose_name ='对方院校/机构名称')
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核',verbose_name ='状态')
    type = models.CharField(max_length = 50,verbose_name ='交换类别')
    nature = models.CharField(max_length = 20,verbose_name ='交流性质')
    score = models.SmallIntegerField(null = True,blank = True,verbose_name ='分数')
    startTime = models.DateField(verbose_name ='开始时间')
    endTime = models.DateField(verbose_name ='结束时间')
    complete = models.PositiveIntegerField(null = True,blank = True,verbose_name ='完成度')
    inspector = models.ForeignKey(Inspectors)
    student = models.ForeignKey(Students)
    SupportText = models.TextField(null = True,blank = True,verbose_name ='支撑文档')#支撑文档 

    def __unicode__(self):
        return self.rankName

#StudentCadre-s
class StudentCadreRank(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核',verbose_name ='状态')
    organizitionType = models.CharField(max_length = 50,verbose_name ='组织类型')
    organizitionName = models.CharField(max_length = 20,verbose_name ='组织名称')
    rankName = models.CharField(max_length = 20,verbose_name ='学生干部名称')
    score = models.SmallIntegerField(null = True,blank = True,verbose_name ='学生干部评分')
    complete = models.PositiveIntegerField(null = True,blank = True,verbose_name ='完成度')
    inspector = models.ForeignKey(Inspectors)
    student = models.ForeignKey(Students)
    SupportText = models.TextField(null = True,blank = True,verbose_name ='支撑文档')#支撑文档 

    def __unicode__(self):
        return self.rankName 

#IdeologyConstruction
class IdeologyConstructionRank(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核',verbose_name ='状态')
    type = models.CharField(max_length = 50,verbose_name ='活动类别')
    rankName = models.CharField(max_length = 20,verbose_name ='活动名称')
    organizer = models.CharField(max_length = 50,verbose_name ='主办方')
    startingTime = models.DateField(verbose_name ='开始时间')
    Location = models.CharField(max_length = 50,verbose_name ='活动地点')
    Content = models.TextField(verbose_name ='活动内容')
    score = models.SmallIntegerField(null = True,blank = True,verbose_name ='活动评分')
    complete = models.PositiveIntegerField(null = True,blank = True,verbose_name ='完成度')
    inspector = models.ForeignKey(Inspectors)
    teacher = models.ForeignKey(Students)
    SupportText = models.TextField(null = True,blank = True,verbose_name ='支撑文档')#支撑文档 

    def __unicode__(self):
        return self.rankName

class IdeologyConstruction(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核',verbose_name ='状态')
    StudentNum =models.ForeignKey(Students,verbose_name ='学号')
    rankNum = models.ForeignKey(IdeologyConstructionRank,verbose_name ='思建活动编号')
    inspector = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)

#Lecture
class LectureRank(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核',verbose_name ='状态')
    type = models.CharField(max_length = 50,verbose_name ='讲座类型')
    rankName = models.CharField(max_length = 20,verbose_name ='讲座名称')
    organizer = models.CharField(max_length = 50,verbose_name ='主办方')
    speaker = models.CharField(max_length = 50,verbose_name ='主讲人')
    startingTime = models.DateField(verbose_name ='开始时间')
    Location = models.CharField(max_length = 50,verbose_name ='讲座地点')
    Content = models.TextField(verbose_name ='内容简介')
    score = models.SmallIntegerField(null = True,blank = True,verbose_name ='讲座评分')
    complete = models.PositiveIntegerField(null = True,blank = True,verbose_name ='完成度')
    teacher = models.ForeignKey(Students)
    inspector = models.ForeignKey(Inspectors)
    SupportText = models.TextField(null = True,blank = True,verbose_name ='支撑文档')#支撑文档 

    def __unicode__(self):
        return self.rankName

class Lecture(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核',verbose_name ='状态',verbose_name ='状态')
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(LectureRank)
    inspector = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)

#Volunteering
class VolunteeringRank(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核',verbose_name ='状态')
    rankName = models.CharField(max_length = 20,verbose_name ='项目名称')
    organizer = models.CharField(max_length = 50,verbose_name ='组织者')
    startingTime = models.DateField(verbose_name ='开始时间')
    Location = models.CharField(max_length = 50,verbose_name ='志愿活动地点')
    volunteerTime = models.PositiveIntegerField(verbose_name ='志愿时间')
    Content = models.TextField(verbose_name ='内容简介')
    score = models.SmallIntegerField(null = True,blank = True,verbose_name ='志愿活动评分')
    complete = models.PositiveIntegerField(null = True,blank = True,verbose_name ='完成度')
    inspector = models.ForeignKey(Inspectors)
    teacher = models.ForeignKey(Students)
    SupportText = models.TextField(null = True,blank = True,verbose_name ='支撑文档')#支撑文档 

    def __unicode__(self):
        return self.rankName

class Volunteering(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核',verbose_name ='状态')
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(VolunteeringRank)
    inspector = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)

#SchoolActivity
class SchoolActivityRank(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核',verbose_name ='状态')
    type = models.CharField(max_length = 50,verbose_name ='校园活动类型')
    rankName = models.CharField(max_length = 20,verbose_name ='活动名称' )
    sponsor = models.CharField(max_length = 50,verbose_name ='承办方')
    organizer = models.CharField(max_length = 50,verbose_name ='主办方')
    startingTime = models.DateField(verbose_name ='开始时间')
    awardLevel = models.CharField(max_length = 50,verbose_name ='奖项')
    score = models.SmallIntegerField(null = True,blank = True,verbose_name ='校园活动分级评分')
    complete = models.PositiveIntegerField(null = True,blank = True,verbose_name ='完成度')
    inspector = models.ForeignKey(Inspectors)
    teacher = models.ForeignKey(Students)
    SupportText = models.TextField(null = True,blank = True,verbose_name ='支撑文档')#支撑文档 

    def __unicode__(self):
        return self.rankName

class SchoolActivity(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核',verbose_name ='状态')
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(SchoolActivityRank)
    inspector = models.ForeignKey(Inspectors)

    def __unicode__(self):
        return str(self.StudentNum)

#Internship
class InternshipRank(models.Model):
    rankName = models.CharField(max_length = 20,verbose_name ='实习名称')
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核',verbose_name ='状态')
    type = models.CharField(max_length = 50,verbose_name ='实习类型')
    InternshipTime = models.DateField(verbose_name ='实习时间')
    score = models.SmallIntegerField(null = True,blank = True,verbose_name ='实习分数')
    complete = models.PositiveIntegerField(null = True,blank = True,verbose_name ='完成度')
    inspector = models.ForeignKey(Inspectors)
    teacher = models.ForeignKey(Students)
    SupportText = models.TextField(null = True,blank = True,verbose_name ='支撑文档')#支撑文档 

    def __unicode__(self):
        return self.rankName 

class Internship(models.Model):
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核',verbose_name ='状态')
    StudentNum =models.ForeignKey(Students)
    rankNum = models.ForeignKey(InternshipRank)
    rankName = models.CharField(max_length = 20,verbose_name ='实习名称')
    Time = models.DateField(verbose_name ='实习时间')
    location = models.CharField(max_length = 50,verbose_name ='实习地点')
    job = models.CharField(max_length = 50,verbose_name ='实习岗位')
    contribution = models.TextField(verbose_name ='贡献')
    report = models.TextField(verbose_name ='实习实践报告')
    appraisal = models.TextField(verbose_name ='实习鉴定')
    score = models.PositiveIntegerField(verbose_name ='成绩')
    inspector = models.ForeignKey(Inspectors)
    
    def __unicode__(self):
        return str(self.StudentNum)