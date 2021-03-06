# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User, AbstractUser
# Create your models here.

statusChoice = (
        ('待审核', '待审核'),
        ('未通过', '未通过'),
        ('通过', '通过'),)

def getVerboseName(str):
    NameDic = {
        'User': u'用户',
        'ResearchProjectRank': u'科研立项',
        'IdeologyConstructionRank': u'思建活动', 
        'LectureRank': u'学术讲座',
        'VolunteeringRank': u'志愿活动',
        'SchoolActivityRank': u'校园活动',
        'PaperRank': u'论文',
        'CompetitionRank': u'学术竞赛',
        'ExchangeRank': u'交流交换',
        'StudentCadreRank': u'学生干部',
        'InternshipRank': u'实习实践',
    }
    return NameDic.get(str, NameError)

class CompleteInformation(models.Model):
    Complete = models.PositiveIntegerField(primary_key = True,verbose_name ='完成度' )
    CompleteExplain = models.TextField(verbose_name ='完成度简介' )

class Complete(models.Model):
    complete1 = models.SmallIntegerField(default = 0)
    complete2 = models.SmallIntegerField(default = 0)
    complete3 = models.SmallIntegerField(default = 0)
    complete4 = models.SmallIntegerField(default = 0)
    complete5 = models.SmallIntegerField(default = 0)
    complete6 = models.SmallIntegerField(default = 0)
    complete7 = models.SmallIntegerField(default = 0)
    complete8 = models.SmallIntegerField(default = 0)
    complete9 = models.SmallIntegerField(default = 0)
    complete0 = models.SmallIntegerField(default = 0)
    complete11 = models.SmallIntegerField(default = 0)
    complete12 = models.SmallIntegerField(default = 0)
    complete13 = models.SmallIntegerField(default = 0)
    complete14 = models.SmallIntegerField(default = 0)
    complete15 = models.SmallIntegerField(default = 0)
    complete16 = models.SmallIntegerField(default = 0)
    complete17 = models.SmallIntegerField(default = 0)
    complete18 = models.SmallIntegerField(default = 0)
    complete19 = models.SmallIntegerField(default = 0)
    complete10 = models.SmallIntegerField(default = 0)
    complete21 = models.SmallIntegerField(default = 0)
    complete22 = models.SmallIntegerField(default = 0)
    complete23 = models.SmallIntegerField(default = 0)
    complete24 = models.SmallIntegerField(default = 0)
    complete25 = models.SmallIntegerField(default = 0)
    complete26 = models.SmallIntegerField(default = 0)
    complete27 = models.SmallIntegerField(default = 0)
    complete28 = models.SmallIntegerField(default = 0)
    complete29 = models.SmallIntegerField(default = 0)
    complete20 = models.SmallIntegerField(default = 0)
    class Meta:
       verbose_name = u'完成度'
       verbose_name_plural = u'完成度'

class Choices(models.Model):
    name = models.CharField(max_length = 50,verbose_name ='评价名称')
    score = models.SmallIntegerField(null = True,blank = True,verbose_name ='分数')
    complete = models.ForeignKey(Complete,verbose_name ='完成度',related_name='choiceComplete')
    class Meta:
        verbose_name = u'评价等级'
        verbose_name_plural = u'评价等级'
    def __unicode__(self):
        return self.name

class Instructor(models.Model):
    user = models.OneToOneField(User,unique=True,verbose_name='用户',related_name='ItoU')
    num = models.PositiveIntegerField(verbose_name ='教工号')
    name = models.CharField(max_length = 20,verbose_name ='姓名')
    sex = models.BooleanField(default= 0,verbose_name ='性别')
    phone = models.BigIntegerField(null = True,blank = True,verbose_name ='手机号码' )
    email = models.EmailField(null = True,blank = True,verbose_name ='电子邮箱')
    school = models.CharField(null = True,blank = True,max_length = 50,verbose_name ='学系') 
    level = models.CharField(null = True,blank = True,max_length = 20,verbose_name ='职称')

    class Meta:
        verbose_name = u'辅导员'
        verbose_name_plural = u'辅导员'

    def __unicode__(self):
        return str(self.id)

class Major(models.Model):
    name = models.CharField(max_length = 50,verbose_name ='专业名称')
    instructor = models.ForeignKey(Instructor,verbose_name='辅导员')
    class Meta:
        verbose_name = u'专业'
        verbose_name_plural = u'专业'
    def __unicode__(self):
        return str(self.name)

class Students(models.Model):
    user = models.OneToOneField(User,unique=True,verbose_name='用户',related_name='StoU')
    StudentNum = models.PositiveIntegerField(primary_key = True,verbose_name ='学号' )
    rankName = models.CharField(max_length = 20,verbose_name ='学生姓名' )
    sex = models.BooleanField(verbose_name ='性别')#初始值
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
    major = models.ForeignKey(Major,verbose_name='专业')
    province = models.CharField(max_length = 50,verbose_name ='生源省份')
    complete = models.ForeignKey(Complete,verbose_name ='完成度',related_name='StoC')
    collegeEntranceExaminationScore = models.PositiveSmallIntegerField(verbose_name ='高考分数')
    class Meta:
        verbose_name = u'学生'
        verbose_name_plural = u'学生'
    def __unicode__(self):
        return str(self.StudentNum)

class Teacher(models.Model):
    user = models.OneToOneField(User,unique=True,verbose_name='用户',related_name='TtoU')
    id = models.PositiveIntegerField(primary_key = True,verbose_name ='教工号' )
    name = models.CharField(max_length = 20,verbose_name ='姓名' )
    sex = models.BooleanField(verbose_name ='性别')#初始值
    phone = models.BigIntegerField(verbose_name ='手机号码' )
    email = models.EmailField(verbose_name ='电子邮箱' )#待修改
    rank = models.CharField(max_length = 50,verbose_name ='职称')
    department = models.CharField(max_length = 50,verbose_name='学系')

class Lesson(models.Model):
    name = models.CharField(max_length = 50,verbose_name ='课程名称')
    num = models.CharField(max_length = 10,verbose_name ='课序号')
    credit = models.PositiveSmallIntegerField(verbose_name ='学分')
    time = models.PositiveIntegerField(verbose_name ='学时')
    introduction = models.CharField(max_length = 200,verbose_name ='课程介绍')
    classTarget = models.CharField(max_length = 200,verbose_name ='课程目标')
    classSort = models.CharField(max_length = 50,verbose_name ='课程类别')
    teacher = models.ForeignKey(Complete,verbose_name ='教师',related_name='LtoT')
    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = u'课程'
    def __unicode__(self):
        return str(self.num)

class Score(models.Model):
    student =models.ForeignKey(Students,verbose_name ='学生学号')
    lesson =models.ForeignKey(Lesson,verbose_name ='课程名称')
    score = models.PositiveSmallIntegerField(verbose_name ='成绩')
    class Meta:
        verbose_name = u'成绩'
        verbose_name_plural = u'成绩'

class CompleteLM(models.Model):
    major =models.ForeignKey(Major,verbose_name ='专业名称')
    lesson =models.ForeignKey(Lesson,verbose_name ='课程名称')
    complete =models.ForeignKey(Complete,verbose_name ='完成度')


class RankLinks(models.Model):
    rtype = models.CharField(max_length = 50,verbose_name ='项目类型')
    rnum = models.PositiveSmallIntegerField(verbose_name ='项目主键')
    status = models.CharField(choices= statusChoice,max_length = 10,default = '待审核',verbose_name ='状态')
    student =models.ForeignKey(Students,verbose_name ='学号',related_name="LtoS")
    choice = models.ForeignKey(Choices,verbose_name ='评价等级',null = True,blank = True)
    class Meta:
       verbose_name = u'活动-学生关系表'
       verbose_name_plural = u'活动-学生关系表'
    def __unicode__(self):
        return u'学号'+str(self.student)+getVerboseName(self.rtype)+u'编号'+str(self.rnum)


#ResearchProject
class ResearchProjectRank(models.Model):
    rankName = models.CharField(max_length = 20,verbose_name ='科研立项名称')
    rank = models.CharField(max_length = 20,verbose_name ='科研立项等级')
    startingTime = models.DateField(verbose_name ='开始时间')
    role = models.CharField(max_length = 20,verbose_name ='身份')
    active = models.BooleanField(default = 1,verbose_name ='可用性')
    class Meta:
        verbose_name = u'科研立项'
        verbose_name_plural = u'科研立项'
    def __unicode__(self):
        return self.rankName

#Lecture
class LectureRank(models.Model):
    type = models.CharField(max_length = 50,verbose_name ='讲座类型')
    rankName = models.CharField(max_length = 20,verbose_name ='讲座名称')
    organizer = models.CharField(max_length = 50,verbose_name ='主办方')
    speaker = models.CharField(max_length = 50,verbose_name ='主讲人')
    startingTime = models.DateField(verbose_name ='开始时间')
    Location = models.CharField(max_length = 50,verbose_name ='讲座地点')
    Content = models.TextField(verbose_name ='内容简介')
    active = models.BooleanField(default = 1,verbose_name ='可用性')
    class Meta:
        verbose_name = u'学术讲座'
        verbose_name_plural = u'学术讲座'
    def __unicode__(self):
        return self.rankName

#Volunteering
class VolunteeringRank(models.Model):
    rankName = models.CharField(max_length = 20,verbose_name ='项目名称')
    organizer = models.CharField(max_length = 50,verbose_name ='组织者')
    startingTime = models.DateField(verbose_name ='开始时间')
    Location = models.CharField(max_length = 50,verbose_name ='志愿活动地点')
    volunteerTime = models.PositiveIntegerField(verbose_name ='志愿时间')
    Content = models.TextField(verbose_name ='内容简介')
    active = models.BooleanField(default = 1,verbose_name ='可用性')
    class Meta:
        verbose_name = u'志愿活动'
        verbose_name_plural = u'志愿活动'
    def __unicode__(self):
        return self.rankName

#SchoolActivity
class SchoolActivityRank(models.Model):
    type = models.CharField(max_length = 50,verbose_name ='校园活动类型')
    rankName = models.CharField(max_length = 20,verbose_name ='活动名称' )
    sponsor = models.CharField(max_length = 50,verbose_name ='承办方')
    organizer = models.CharField(max_length = 50,verbose_name ='主办方')
    startingTime = models.DateField(verbose_name ='开始时间')
    awardLevel = models.CharField(max_length = 50,verbose_name ='奖项')
    active = models.BooleanField(default = 1,verbose_name ='可用性')
    class Meta:
        verbose_name = u'校园活动'
        verbose_name_plural = u'校园活动'
    def __unicode__(self):
        return self.rankName

#IdeologyConstruction
class IdeologyConstructionRank(models.Model):
    type = models.CharField(max_length = 50,verbose_name ='活动类别')
    rankName = models.CharField(max_length = 20,verbose_name ='活动名称')
    organizer = models.CharField(max_length = 50,verbose_name ='主办方')
    startingTime = models.DateField(verbose_name ='开始时间')
    Location = models.CharField(max_length = 50,verbose_name ='活动地点')
    Content = models.TextField(default = '',verbose_name = '活动内容')
    active = models.BooleanField(default = 1,verbose_name ='可用性')
    class Meta:
        verbose_name = u'思建活动'
        verbose_name_plural = u'思建活动'
    def __unicode__(self):
        return self.rankName

#Paper-s
class PaperRank(models.Model):
    rankName = models.CharField(max_length = 50,verbose_name ='论文名称')
    journalName = models.CharField(max_length = 20,verbose_name ='期刊名称')
    rank = models.CharField(max_length = 20,verbose_name ='论文等级')
    AuthorRanking = models.SmallIntegerField(verbose_name ='作者顺序')
    startingTime = models.DateField(verbose_name ='开始时间')
    active = models.BooleanField(default = 1,verbose_name ='可用性')
    class Meta:
        verbose_name = u'论文'
        verbose_name_plural = u'论文'
    def __unicode__(self):
        return self.rankName
#Competition-s
class CompetitionRank(models.Model):
    rankName = models.CharField(max_length = 50,verbose_name ='学术竞赛名称')
    Level = models.CharField(max_length = 20,verbose_name ='学术竞赛等级')
    rank = models.CharField(max_length = 20,verbose_name ='学生排名')
    startingTime = models.DateField(verbose_name ='开始时间')
    active = models.BooleanField(default = 1,verbose_name ='可用性')
    class Meta:
        verbose_name = u'学术竞赛'
        verbose_name_plural = u'学术竞赛'
    def __unicode__(self):
        return self.rankName
#Exchange-s
class ExchangeRank(models.Model):
    rankName = models.CharField(max_length = 50,verbose_name ='对方院校/机构名称')
    type = models.CharField(max_length = 50,verbose_name ='交换类别')
    nature = models.CharField(max_length = 20,verbose_name ='交流性质')
    startTime = models.DateField(verbose_name ='开始时间')
    endTime = models.DateField(verbose_name ='结束时间')
    active = models.BooleanField(default = 1,verbose_name ='可用性')
    class Meta:
        verbose_name = u'交流交换'
        verbose_name_plural = u'交流交换'
    def __unicode__(self):
        return self.rankName
#StudentCadre-s
class StudentCadreRank(models.Model):
    organizitionType = models.CharField(max_length = 50,verbose_name ='组织类型')
    organizitionName = models.CharField(max_length = 20,verbose_name ='组织名称')
    rankName = models.CharField(max_length = 20,verbose_name ='学生干部名称')
    active = models.BooleanField(default = 1,verbose_name ='可用性')
    class Meta:
        verbose_name = u'学生干部'
        verbose_name_plural = u'学生干部'
    def __unicode__(self):
        return self.rankName 
#Internship-s
class InternshipRank(models.Model):
    rankName = models.CharField(max_length = 20,verbose_name ='实习名称')
    type = models.CharField(max_length = 50,verbose_name ='实习类型')
    Time = models.DateField(verbose_name ='实习时间')
    location = models.CharField(max_length = 50,verbose_name ='实习地点')
    job = models.CharField(max_length = 50,verbose_name ='实习岗位')
    contribution = models.TextField(verbose_name ='贡献')
    report = models.TextField(verbose_name ='实习实践报告')
    appraisal = models.TextField(verbose_name ='实习鉴定')
    active = models.BooleanField(default = 1,verbose_name ='可用性')
    class Meta:
       verbose_name = u'实习实践'
       verbose_name_plural = u'实习实践'
    def __unicode__(self):
        return self.rankName 