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
from app.type import *
from app.Info import *
from app.project import *
from app.complete import GetComplete
from django.http import HttpResponse
from django.http import HttpResponseRedirect  
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required  
import random,time
import MySQLdb
from django.template.context import Context
import sys
from django.core.files.uploadedfile import TemporaryUploadedFile
import os
from deco import *
from app.excel import *
from django.contrib.contenttypes.models import ContentType
reload(sys)
sys.setdefaultencoding("utf-8")
import DjangoWebProject.settings

def NewWeb():
    if not Permission.objects.filter(codename = 'is_instructor'): 
        Permission.objects.create(name=u'是否为辅导员',content_type = ContentType.objects.get_for_model(User),codename='is_instructor')

@teacher_required
def Excel(request):
    if request.method == 'POST' and request.POST.has_key('register'):
        myFile = request.FILES.get("register", None)    # 获取上传的文件，如果没有文件，则默认为None  
        if not myFile:  
            return HttpResponse("no files for upload!") 
        if ExcelRegister(myFile.temporary_file_path()):
            return HttpResponse("over!")  
        return HttpResponse("error")
    elif request.method == 'POST' and request.POST.has_key('lesson'):
        myFile = request.FILES.get("lesson", None)
        if not myFile:  
            return HttpResponse("no files for upload!") 
        if ExcelImportLesson(myFile.temporary_file_path()):
            return HttpResponse("over!")  
        return HttpResponse("error")
    else:
        assert isinstance(request, HttpRequest)
        return render(request,'app/excel.html',{})

'''思建活动(目前用于测试)
'''
#创建
@login_required
def CreateIdeologyConstruction(request): 
    error = []
    try:
            student = Students.objects.get(user = request.user)
            project = IdeologyConstructionRank.objects.filter(teacher = student)
    except Exception,e:
            error.append(e)
    if request.method == 'POST':
        form = CreateIdeologyConstructionForm(request.POST)
        if form.is_valid():
                cd = form.cleaned_data
                project = IdeologyConstructionRank(teacher = student,
                                status = '待审核',
                                rankName = cd['ProjectName'],
                                startingTime = cd['startingTime'],
                                type = cd['type'],
                                Location = cd['Location'],
                                organizer = cd['organizer'],
                                Content = cd['Content'],
                                SupportText = cd['SupportText'])
                project.save()
                return render_with_type_(request,'first.html',{'alert':['okkkk!']})
        else:
            error.append('请确认是否已经输入相关信息')
    else:
        form = CreateIdeologyConstructionForm()
    return render_with_type_(request,'Create/createIdeologyConstruction.html',{'form':form,'alert':error})
@login_required
def IdeologyConstructionCheck(request,id): return ProjectCheck(IdeologyConstructionRank,IdeologyConstruction,IdeologyConstructionForm,request,id)
@login_required
def IdeologyConstructionDetail(request,id): return ProjectDetail(IdeologyConstructionRank,IdeologyConstruction,request,id,None)
@login_required
def JoinIdeologyConstruction(request,id): return ProjectJoin(IdeologyConstructionRank,IdeologyConstruction,request,id)
@login_required
def IdeologyConstructionIndex(request): return ProjectIndex(IdeologyConstructionRank,IdeologyConstruction,request,None)
@login_required
def AddIdeologyConstruction(request,id,sid): return ProjectAdd(IdeologyConstructionRank,IdeologyConstruction,request,id,sid)
@login_required
def DeleteIdeologyConstruction(request,id): return ProjectDelete(IdeologyConstructionRank,IdeologyConstruction,request,id)
    


def ShowComplete(request):
    error = None
    student = Students.objects.get(user = request.user)
    complete = GetComplete(request,student)
    fields = Complete._meta.fields
    FieldProject = {}
    for field in fields :
        if field.name != 'id': FieldProject[field.verbose_name] = getattr(complete,field.name) #键值对
    return render_with_type_(request,'complete.html', {'complete': FieldProject})
    

def construction(request):
    return render_with_type_(request,'app/construction.html',{})

def home(request):
    NewWeb()
    assert isinstance(request, HttpRequest)
    if request.user.is_authenticated():
        return render(request,'app/index.html',{})
    else:
        return redirect('/login')

def first(request):
    return render(request,'first.html')

def shit(request):
    return render_with_type_(request,'app/shit.html',{})

def contact(request):
    return render_with_type_(request,'app/contact.html', {'t': settings.STATIC_ROOT})

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })

def search_form(request):
    return render_with_type_(request,'search_form.html',{})

def search(request):
    if 'q' in request.GET:#GET是一个dict，使用文本框的name作为key
    #在这里需要做一个判断，是否存在提交数据，以免报错
        q = request.GET['q']
        #使用lookup后缀，意思为书名不区分大小写，包含q就可以
        users = User.objects.filter(username__icontains=q)
        return render_with_type_(request,'search_results.html', {'users' : users, 'query':q})
    else:
        message = 'You submitted an empty form.'
        #只是简单的返回一个response对象，因为没有使用模块，所以也不用渲染数据Context
        return HttpResponse(message)

def reset(request):
    #可以不写，因为python中if中定义的变量，也可以在整个函数中可见
    form = None 
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                student = Students.objects.get(user = User.objects.get(username=cd['username'],email=cd['email']))
            except Exception,e:
                return render_with_type_(request,'reset_form.html', {'form': form,'alert':e})
            if student.StudentNum == cd['StudentNum'] and str(student.identityNumber)[-6:] == cd['IdentityNumberSix']:
                user.password = make_password(cd['password'])
                return HttpResponseRedirect('/login')
    else:
        form = ResetPasswordForm()
    return render_with_type_(request,'reset_form.html', {'form': form})

def changepassword(request,username):
	error = None
	if request.method == 'POST':
		form = ChangepwdForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			user = authenticate(username=username,password=data['old_pwd'])
			if user is not None:
				if data['new_pwd'] == data['new_pwd2']:
					newuser = User.objects.get(username__exact=username)
					newuser.set_password(data['new_pwd'])
					newuser.save()
					return HttpResponseRedirect('/login/')
				else:
					error.append('Please input the same password')
			else:
				error.append('Please correct the old password')
		else:
			error.append('Please input the required domain')
	else:
		form = ChangepwdForm()
	return render_with_type_(request,'changepassword.html',{'form':form,'alert':error})

def createPaper(request):
    if request.method == 'POST':
        error = None
        getInfo(request)
        student = getInfo(request)['student']
        form = CreatePaperForm(request.POST)
        if form.is_valid():
            #try:
                cd = form.cleaned_data
                project = PaperRank(rankName = cd['ProjectName'],
                                journalName = cd['JournalName'],
                                student = student,
                                startingTime = cd['ProjectTime'],
                                AuthorRanking = cd['AuthorRanking'],
                                status = '待审核',
                                rank = '',
                                )
                project.save()
                return render_with_type_(request,'first.html',{'alert':'okkkk!'})
            #except Exception,e:
                error = e
        else:
            error.append('Please input information of your project')
    else:
        form = CreatePaperForm()
        error = None
    return render_with_type_(request,'Create/createPaper.html',{'form':form,'alert':error})
def paper(request,id):
    error = None
    try:  
        project = PaperRank.objects.get(id = int(id))
    except Exception,e:  
        error = e
        return render_with_type_(request,'Paper.html',{'alert':error})
    if project.status == '待审核' and request.user.has_perm('auth.is_instructor'):
        if request.method == 'POST':
            form = PaperForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                try:
                    choice = Choices.objects.get(id = cd['level'])
                    project.score = choice.score
                    project.complete = choice.complete
                    if request.POST.has_key('passyes'):
                        project.status = '通过'
                    elif request.POST.has_key('passno'):
                        project.status = '未通过'
                    project.save()
                    return render_with_type_(request,'Index/PaperIndex.html',{'projects':PaperRank.objects.filter(status = '待审核'),'alert':'审核成功！','can':True})
                except Exception,e:  
                    error = e
            else:
                error.append('Please input information of your project')
        else:
            form = PaperForm()
        return render_with_type_(request,'Paper.html',{'form':form,'project':project})
    elif request.user.has_perm('auth.is_instructor'):
       return render_with_type_(request,'Index/PaperIndex.html',{'projects':PaperRank.objects.filter(status = '待审核'),'alert':'审核失败！该活动已审核','can':True})
    return render_with_type_(request,'Index/PaperIndex.html',{'projects':PaperRank.objects.filter(status = '通过'),'can':False})
def paperIndex(request):
    getInfo(request)
    student = getInfo(request)['student']
    if request.user.has_perm('auth.is_instructor'):
        return render_with_type_(request,'Index/PaperIndex.html',{'projects':PaperRank.objects.filter(status = '待审核')})#teacher
    return render_with_type_(request,'index.html',{'alert':'你没有权限审核！请与管理员联系'})
def createCompetition(request):
    if request.method == 'POST':
        error = None
        getInfo(request)
        student = getInfo(request)['student']
        form = CreateCompetitionForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = CompetitionRank(rankName = cd['ProjectName'],
                                student = student,
                                startingTime = cd['ProjectTime'],
                                status = '待审核',
                                level = cd['level'],
                                rank = cd['rank'],)
                project.save()
                return render_with_type_(request,'first.html',{'alert':'okkkk!'})
            except Exception,e:
                error = e
        else:
            error.append('Please input information of your project')
    else:
        form = CreateCompetitionForm()
        error = None
    return render_with_type_(request,'Create/createCompetition.html',{'form':form,'alert':error})
def competition(request,id):
    error = None
    try:  
        project = CompetitionRank.objects.get(id = int(id))
    except Exception,e:  
        error = e
        return render_with_type_(request,'Competition.html',{'alert':error})
    if project.status == '待审核' and request.user.has_perm('auth.is_instructor'):
        if request.method == 'POST':
            form = CompetitionForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                try:
                    choice = Choices.objects.get(id = cd['level'])
                    project.score = choice.score
                    project.complete = choice.complete
                    if request.POST.has_key('passyes'):
                        project.status = '通过'
                    elif request.POST.has_key('passno'):
                        project.status = '未通过'
                     
                    project.save()
                    return render_with_type_(request,'Index/CompetitionIndex.html',{'projects':CompetitionRank.objects.filter(status = '待审核'),'alert':'审核成功！','can':True})
                except Exception,e:  
                    error = e
            else:
                error.append('Please input information of your project')
        else:
            form = CompetitionForm()
        return render_with_type_(request,'Competition.html',{'form':form,'project':project})
    elif request.user.has_perm('auth.is_instructor'):
       return render_with_type_(request,'Index/CompetitionIndex.html',{'projects':CompetitionRank.objects.filter(status = '待审核'),'alert':'审核失败！该活动已审核','can':True})
    return render_with_type_(request,'Index/CompetitionIndex.html',{'projects':CompetitionRank.objects.filter(status = '通过'),'can':False})
def competitionIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = CompetitionRank.objects.filter(student = student.StudentNum)
    except Exception,e: 
        return render_with_type_(request,'index.html',{'alert':e})
    if request.user.has_perm('auth.is_instructor'):
        return render_with_type_(request,'Index/CompetitionIndex.html',{'projects':CompetitionRank.objects.filter(status = '待审核')})#teacher
    return render_with_type_(request,'index.html',{'alert':'你没有权限审核！请与管理员联系'})
def createStudentCadre(request):
    if request.method == 'POST':
        error = None
        try:
            student = Students.objects.get(user = request.user)
            
        except Exception,e:
            error = e
        form = CreateStudentCadreForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = StudentCadreRank(teacher = student,
                                organizitionType = cd['organizitionType'],
                                organizitionName = cd['organizitionName'],
                                status = '待审核',
                               )
                project.save()
                return render_with_type_(request,'first.html',{'alert':'okkkk!'})
            except Exception,e:
                error = e
        else:
            error.append('Please input information of your project')
    else:
        form = CreateStudentCadreForm()
        error = None
    return render_with_type_(request,'Create/createStudentCadre.html',{'form':form,'alert':error})
def studentCadre(request,id):
    error = None
    try:  
        project = StudentCadreRank.objects.get(id = int(id))
    except Exception,e:  
        error = e
        return render_with_type_(request,'StudentCadre.html',{'alert':error})
    if project.status == '待审核' and request.user.has_perm('auth.is_instructor'):
        if request.method == 'POST':
            form = StudentCadreForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                try:
                    choice = Choices.objects.get(id = cd['level'])
                    project.score = choice.score
                    project.complete = choice.complete
                    if request.POST.has_key('passyes'):
                        project.status = '通过'
                    elif request.POST.has_key('passno'):
                        project.status = '未通过'
                    project.save()
                    return render_with_type_(request,'Index/StudentCadreIndex.html',{'projects':StudentCadreRank.objects.filter(status = '待审核'),'alert':'审核成功！','can':True})
                except Exception,e:  
                    error = e
            else:
                error.append('Please input information of your project')
        else:
            form = StudentCadreForm()
        return render_with_type_(request,'StudentCadre.html',{'form':form,'project':project})
    elif request.user.has_perm('auth.is_instructor'):
       return render_with_type_(request,'Index/StudentCadreIndex.html',{'projects':StudentCadreRank.objects.filter(status = '待审核'),'alert':'审核失败！该活动已审核','can':True})
    return render_with_type_(request,'Index/StudentCadreIndex.html',{'projects':StudentCadreRank.objects.filter(status = '通过'),'can':False})
def studentCadreIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = StudentCadreRank.objects.filter(student = student.StudentNum)
    except Exception,e: 
        return render_with_type_(request,'index.html',{'alert':e})
    if request.user.has_perm('auth.is_instructor'):
        return render_with_type_(request,'Index/StudentCadreIndex.html',{'projects':StudentCadreRank.objects.filter(status = '待审核')})#teacher
    return render_with_type_(request,'index.html',{'alert':'你没有权限审核！请与管理员联系'})
def createExchange(request):
    if request.method == 'POST':
        error = None
        #try:
        student = Students.objects.get(user = request.user)
        
        #except Exception,e:#error = e
        form = CreateExchangeForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = ExchangeRank(rankName = cd['ProjectName'],
                                type = cd['type'],
                                nature = cd['nature'],
                                student = student,
                                startTime = cd['startTime'],
                                endTime = cd['endTime'],
                                status = '待审核',
                                
                                
                               )
                project.save()
                return render_with_type_(request,'first.html',{'alert':'okkkk!'})
            except Exception,e:
                error = e
        else:
            error.append('Please input information of your project')
    else:
        form = CreateExchangeForm()
        error = None
    return render_with_type_(request,'Create/createExchange.html',{'form':form,'alert':error})
def exchange(request,id):
    error = None
    try:  
        project = ExchangeRank.objects.get(id = int(id))
    except Exception,e:  
        error = e
        return render_with_type_(request,'Exchange.html',{'alert':error})
    if project.status == '待审核' and request.user.has_perm('auth.is_instructor'):
        if request.method == 'POST':
            form = ExchangeForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                try:
                    choice = Choices.objects.get(id = cd['level'])
                    project.score = choice.score
                    project.complete = choice.complete
                    if request.POST.has_key('passyes'):
                        project.status = '通过'
                    elif request.POST.has_key('passno'):
                        project.status = '未通过'
                     
                    project.save()
                    return render_with_type_(request,'Index/ExchangeIndex.html',{'projects':ExchangeRank.objects.filter(status = '待审核'),'alert':'审核成功！','can':True})
                except Exception,e:  
                    error = e
            else:
                error.append('Please input information of your project')
        else:
            form = ExchangeForm()
        return render_with_type_(request,'Exchange.html',{'form':form,'project':project})
    elif request.user.has_perm('auth.is_instructor'):
       return render_with_type_(request,'Index/ExchangeIndex.html',{'projects':ExchangeRank.objects.filter(status = '待审核'),'alert':'审核失败！该活动已审核','can':True})
    return render_with_type_(request,'Index/ExchangeIndex.html',{'projects':ExchangeRank.objects.filter(status = '通过'),'can':False})
def exchangeIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = ExchangeRank.objects.filter(student = student.StudentNum)
    except Exception,e: 
        return render_with_type_(request,'index.html',{'alert':e})
    if request.user.has_perm('auth.is_instructor'):
        return render_with_type_(request,'Index/ExchangeIndex.html',{'projects':ExchangeRank.objects.filter(status = '待审核')})#teacher
    return render_with_type_(request,'index.html',{'alert':'你没有权限审核！请与管理员联系'})


'''科研立项
'''
#创建
def createResearchProject(request):
    if request.method == 'POST':
        error = None
        try:
            student = Students.objects.get(user = request.user)
            
        except Exception,e:
            error = e
        form = CreateResearchProjectForm(request.POST)
        if form.is_valid():
            #try:
                cd = form.cleaned_data
                project = ResearchProjectRank(rankName = cd['ProjectName'],teacher = student,startingTime = cd['ProjectTime'],status = '待审核',rank = '',)
                project.save()
                return render_with_type_(request,'first.html',{'alert':'okkkk!'})
            #except Exception,e:
                error = e
        else:
            error = 'Please input information of your project'
    else:
        form = CreateResearchProjectForm()
        error = None
    return render_with_type_(request,'Create/createResearchProject.html',{'form':form,'alert':error})
#评价审核（审核结果输入）
def researchProject(request,id):
    try:  
        project = ResearchProjectRank.objects.get(id = int(id))
    except Exception,e:  
        return render_with_type_(request,'ResearchProject.html',{'alert':e})
    if project.status == '待审核' and request.user.has_perm('auth.is_instructor'):
        if request.method == 'POST':
            form = ResearchProjectForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                try:
                    choice = Choices.objects.get(id = cd['level'])
                    project.rank = Choices.objects.get(id = cd['level']).name
                    project.MemberScore = choice.memberScore
                    project.ManagerScore = choice.managerScore
                    project.memberComplete = choice.memberComplete
                    project.managerComplete = choice.managerComplete
                    if request.POST.has_key('passyes'):
                        project.status = '通过'
                    elif request.POST.has_key('passno'):
                        project.status = '未通过'
                    else :
                        return render_with_type_(request,'ResearchProject.html',{'form':form,'project':project,'alert':'某还没命名的错误'})
                    
                    project.save()
                    return render_with_type_(request,'Index/ResearchProjectIndex.html',{'projects':ResearchProjectRank.objects.filter(status = '待审核'),'alert':'科研立项审核成功！','can':True})
                except Exception,e:  
                    error = e
            else:
                error = 'Please input information of your project'
        else:
            form = ResearchProjectForm()
            e = None
        return render_with_type_(request,'ResearchProject.html',{'form':form,'project':project,'alert':e})
    elif request.user.has_perm('auth.is_instructor'):
       return render_with_type_(request,'Index/ResearchProjectIndex.html',{'projects':ResearchProjectRank.objects.filter(status = '待审核'),'alert':'科研立项审核失败！该活动已审核','can':True})
    return render_with_type_(request,'Index/ResearchProjectIndex.html',{'projects':ResearchProjectRank.objects.filter(status = '通过'),'can':False})
#项目详情
def ResearchProjectDetail(request,id):
    try:  
        project = ResearchProjectRank.objects.get(id = int(id))
    except Exception,e: 
        return render_with_type_(request,'ResearchProjectDetail.html',{'alert':e})
    return render_with_type_(request,'ResearchProjectDetail.html',{'project':project})
#申请加入
def JoinResearchProject(request,id):
    alert = ''
    try:  
        project = ResearchProjectRank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
    except Exception,e:  
        return render_with_type_(request,'ResearchProjectDetail.html',{'alert':e})
    join = ResearchProject(status = '待审核',StudentNum = student ,rankNum = project )
    join.save()
    alert = '成功加入！'
    return render_with_type_(request,'Index/ResearchProjectIndex.html',{'alert':alert})
#申请者的列表
def ResearchProjectIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = ResearchProject.objects.filter(StudentNum= student)
    except Exception,e: 
        return render_with_type_(request,'index.html',{'alert':e})
    if request.user.has_perm('auth.is_instructor'):
        return render_with_type_(request,'Index/researchProjectIndex.html',{'projects':ResearchProjectRank.objects.filter(status = '待审核'),'can':True})
    if project.count() == 0:
        return render_with_type_(request,'Index/researchProjectIndex.html',{'projects':ResearchProjectRank.objects.filter(status = '通过'),'can':False})
    return render_with_type_(request,'index.html',{'projects':ResearchProject.objects.filter(StudentNum = student),'alert':'您已加入科研立项!'})
#管理申请的列表
def ResearchProjectList(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = ResearchProjectRank.objects.get(teacher = student)
        joins = ResearchProject.objects.filter(rankNum = project)
    except Exception,e: 
        return render_with_type_(request,'ResearchProjectList.html',{'alert':e})
    return render_with_type_(request,'ResearchProjectList.html',{'projects':joins})
#申请者的详情
def ResearchProjectSDetail(request,id):
    try:  
        join = ResearchProject.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type_(request,'ResearchProjectSDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        return render_with_type_(request,'ResearchProjectSDetail.html',{'project':join,'student':student})
    return render_with_type_(request,'ResearchProjectSDetail.html',{'alert':'您无权查看此报名信息！'})
#审核加入
def CheckResearchProject(request,id,isok):
    try:  
        join = ResearchProject.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type_(request,'ResearchProjectSDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        if isok:
            join.status = '通过'
        else:
            join.status = '未通过'
        join.save()
    return render_with_type_(request,'ResearchProjectSDetail.html',{'alert':'您无权审核此报名信息！'})



'''讲座
'''
#创建
def createLecture(request):
    if request.method == 'POST':
        error = None
        try:
            student = Students.objects.get(user = request.user)
            
        except Exception,e:
            error = e
        form = CreateLectureForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = LectureRank(rankName = cd['ProjectName'],
                                type = cd['type'],
                                teacher = student,
                                startingTime = cd['startingTime'],
                                organizer = cd['organizer'],
                                speaker = cd['speaker'],
                                Location = cd['Location'],
                                Content = cd['Content'],
                                status = '待审核')
                project.save()
                return render_with_type_(request,'first.html',{'alert':'okkkk!'})
            except Exception,e:
                error = e
        else:
            error.append('Please input information of your project')
    else:
        form = CreateLectureForm()
        error = None
    return render_with_type_(request,'Create/createLecture.html',{'form':form,'alert':error})
#评价审核（审核结果输入）
def lecture(request,id):
    error = None
    try:  
        project = LectureRank.objects.get(id = int(id))
    except Exception,e:  
        error = e
        return render_with_type_(request,'IdeologyConstruction.html',{'alert':error})
    if project.status == '待审核':
        if request.method == 'POST':
            form = LectureForm(request.POST)
            if form.is_valid() and request.user.has_perm('auth.is_instructor'):
                cd = form.cleaned_data
                try:
                    choice = Choices.objects.get(id = cd['level'])
                    project.score = choice.score
                    project.complete = choice.complete
                    if request.POST.has_key('passyes'):
                        project.status = '通过'
                    elif request.POST.has_key('passno'):
                        project.status = '未通过'
                    
                    project.save()
                    return render_with_type_(request,'Index/LectureIndex.html',{'projects':LectureRank.objects.filter(status = '待审核'),'alert':'讲座活动审核成功！','can':True})
                except Exception,e:  
                    error = e
            else:
                error.append('Please input information of your project')
        else:
            form = LectureForm()
            return render_with_type_(request,'Lecture.html',{'form':form,'project':project})
    elif request.user.has_perm('auth.is_instructor'):
       return render_with_type_(request,'Index/LectureIndex.html',{'projects':LectureRank.objects.filter(status = '待审核'),'alert':'讲座活动审核失败！该活动已审核','can':True})
    return render_with_type_(request,'Index/LectureIndex.html',{'projects':LectureRank.objects.filter(status = '通过'),'can':False})
#项目详情
def LectureDetail(request,id):
    try:  
        project = LectureRank.objects.get(id = int(id))
    except Exception,e: 
        return render_with_type_(request,'LectureDetail.html',{'alert':e})
    return render_with_type_(request,'LectureDetail.html',{'project':project})
#申请加入
def JoinLecture(request,id):
    alert = ''
    try:  
        project = LectureRank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
    except Exception,e:  
        return render_with_type_(request,'LectureDetail.html',{'alert':e})
    join = Lecture(status = '待审核',StudentNum = student ,rankNum = project )
    join.save()
    alert = '成功加入！'
    return render_with_type_(request,'Index/LectureIndex.html',{'alert':alert})
#申请者的列表
def LectureIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = Lecture.objects.filter(StudentNum= student)
    except Exception,e: 
        return render_with_type_(request,'index.html',{'lectures':Lecture.objects.filter(StudentNum = student),'alert':e})
    if request.user.has_perm('auth.is_instructor'):
        return render_with_type_(request,'Index/LectureIndex.html',{'projects':LectureRank.objects.filter(status = '待审核'),'can':True})
    return render_with_type_(request,'Index/LectureIndex.html',{'projects':LectureRank.objects.filter(status = '通过'),'can':False})
#管理申请的列表
def LectureList(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = LectureRank.objects.get(teacher = student)
        joins = Lecture.objects.filter(rankNum = project)
    except Exception,e: 
        return render_with_type_(request,'LectureList.html',{'alert':e})
    return render_with_type_(request,'LectureList.html',{'projects':joins})
#申请者的详情
def LectureSDetail(request,id):
    try:  
        join = Lecture.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type_(request,'LectureSDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        return render_with_type_(request,'LectureSDetail.html',{'project':join,'student':student})
    return render_with_type_(request,'LectureSDetail.html',{'alert':'您无权查看此报名信息！'})
#审核加入
def CheckLecturex(request,id,isok):
    try:  
        join = Lecture.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type_(request,'LectureSDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        if isok:
            join.status = '通过'
        else:
            join.status = '未通过'
        join.save()
    return render_with_type_(request,'LectureSDetail.html',{'alert':'您无权审核此报名信息！'})


'''志愿活动
'''
#创建
def createVolunteering(request):
    if request.method == 'POST':
        error = None
        try:
            student = Students.objects.get(user = request.user)
        except Exception,e:
            error = e
        form = CreateVolunteeringForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = VolunteeringRank(rankName = cd['ProjectName'],
                                teacher = Students.objects.get(user = request.user),
                                startingTime = cd['startingTime'],
                                volunteerTime = cd['volunteerTime'],
                                organizer = cd['organizer'],
                                Location = cd['Location'],
                                Content = cd['Content'],
                                status = '待审核')
                project.save()
                return render_with_type_(request,'first.html',{'alert':'okkkk!'})
            except Exception,e:
                error = e
        else:
            error.append('Please input information of your project')
    else:
        form = CreateVolunteeringForm()
        error = None
    return render_with_type_(request,'Create/createVolunteering.html',{'form':form,'alert':error})
#评价审核（审核结果输入）
def volunteering(request,id):
    error = None
    try:  
        project = VolunteeringRank.objects.get(id = int(id))
    except Exception,e:  
        error = e
        return render_with_type_(request,'Volunteering.html',{'alert':error})
    if project.status == '待审核':
        if request.method == 'POST':
            form = VolunteeringForm(request.POST)
            if form.is_valid() and request.user.has_perm('auth.is_instructor'):
                cd = form.cleaned_data
                try:
                    choice = Choices.objects.get(id = cd['level'])
                    project.score = choice.score
                    project.complete = choice.complete
                    if request.POST.has_key('passyes'):
                        project.status = '通过'
                    elif request.POST.has_key('passno'):
                        project.status = '未通过'
                    
                    project.save()
                    return render_with_type_(request,'Index/VolunteeringIndex.html',{'projects':VolunteeringRank.objects.filter(status = '待审核'),'alert':'志愿活动审核成功！','can':True})
                except Exception,e:  
                    error = e
            else:
                error.append('Please input information of your project')
        else:
            form = VolunteeringForm()
            return render_with_type_(request,'Lecture.html',{'form':form,'project':project})
    elif request.user.has_perm('auth.is_instructor'):
       return render_with_type_(request,'Index/VolunteeringIndex.html',{'projects':VolunteeringRank.objects.filter(status = '待审核'),'alert':'志愿活动审核失败！该活动已审核','can':True})
    return render_with_type_(request,'Index/VolunteeringIndex.html',{'projects':VolunteeringRank.objects.filter(status = '通过'),'can':False})
#项目详情
def VolunteeringDetail(request,id):
    try:  
        project = VolunteeringRank.objects.get(id = int(id))
    except Exception,e: 
        return render_with_type_(request,'VolunteeringDetail.html',{'alert':e})
    return render_with_type_(request,'VolunteeringDetail.html',{'project':project})
#申请加入
def JoinVolunteering(request,id):
    alert = ''
    try:  
        project = VolunteeringRank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
    except Exception,e:  
        return render_with_type_(request,'VolunteeringDetail.html',{'alert':e})
    join = Volunteering(status = '待审核',StudentNum = student ,rankNum = project )
    join.save()
    alert = '成功加入！'
    return render_with_type_(request,'Index/VolunteeringIndex.html',{'alert':alert})
#申请者的列表
def VolunteeringIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = Volunteering.objects.filter(StudentNum= student)
    except Exception,e: 
        return render_with_type_(request,'index.html',{'volunteerings':Volunteering.objects.filter(StudentNum = student),'alert':e})
    if request.user.has_perm('auth.is_instructor'):
        return render_with_type_(request,'Index/VolunteeringIndex.html',{'projects':VolunteeringRank.objects.filter(status = '待审核'),'can':True})
    return render_with_type_(request,'Index/VolunteeringIndex.html',{'projects':VolunteeringRank.objects.filter(status = '通过'),'can':False})
#管理申请的列表
def VolunteeringList(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = VolunteeringRank.objects.get(teacher = student)
        joins = Volunteering.objects.filter(rankNum = project)
    except Exception,e: 
        return render_with_type_(request,'VolunteeringList.html',{'alert':e})
    return render_with_type_(request,'VolunteeringList.html',{'projects':joins})
#申请者的详情
def VolunteeringSDetail(request,id):
    try:  
        join = Volunteering.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type_(request,'VolunteeringSDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        return render_with_type_(request,'VolunteeringSDetail.html',{'project':join,'student':student})
    return render_with_type_(request,'VolunteeringSDetail.html',{'alert':'您无权查看此报名信息！'})
#审核加入
def CheckVolunteeringx(request,id,isok):
    try:  
        join = Volunteering.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type_(request,'VolunteeringSDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        if isok:
            join.status = '通过'
        else:
            join.status = '未通过'
        join.save()
    return render_with_type_(request,'VolunteeringSDetail.html',{'alert':'您无权审核此报名信息！'})


'''校园活动
'''
#创建
def createSchoolActivity(request):
    if request.method == 'POST':
        error = None
        try:
            student = Students.objects.get(user = request.user)
        except Exception,e:
            error = e
        form = CreateSchoolActivityForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = SchoolActivityRank(rankName = cd['ProjectName'],
                                teacher = student,
                                startingTime = cd['startingTime'],
                                type = cd['type'],
                                sponsor = cd['sponsor'],
                                organizer = cd['organizer'],
                                awardLevel = cd['awardLevel'],
                                status = '待审核')
                project.save()
                return render_with_type_(request,'first.html',{'alert':'okkkk!'})
            except Exception,e:
                error = e
        else:
            error.append('Please input information of your project')
    else:
        form = CreateSchoolActivityForm()
        error = None
    return render_with_type_(request,'Create/createSchoolActivity.html',{'form':form,'alert':error})
#评价审核（审核结果输入）
def schoolActivity(request,id):
    error = None
    try:  
        project = SchoolActivityRank.objects.get(id = int(id))
    except Exception,e:  
        error = e
        return render_with_type_(request,'SchoolActivity.html',{'alert':error})
    if project.status == '待审核':
        if request.method == 'POST':
            form = SchoolActivityForm(request.POST)
            if form.is_valid() and request.user.has_perm('auth.is_instructor'):
                cd = form.cleaned_data
                try:
                    choice = Choices.objects.get(id = cd['level'])
                    project.score = choice.score
                    project.complete = choice.complete
                    if request.POST.has_key('passyes'):
                        project.status = '通过'
                    elif request.POST.has_key('passno'):
                        project.status = '未通过'
                    project.save()
                    return render_with_type_(request,'Index/SchoolActivityIndex.html',{'projects':SchoolActivityRank.objects.filter(status = '待审核'),'alert':'校园活动审核成功！','can':True})
                except Exception,e:  
                    error = e
            else:
                error.append('Please input information of your project')
        else:
            form = SchoolActivityForm()
            return render_with_type_(request,'schoolActivity.html',{'form':form,'project':project})
    elif request.user.has_perm('auth.is_instructor'):
       return render_with_type_(request,'Index/SchoolActivityIndex.html',{'projects':SchoolActivityRank.objects.filter(status = '待审核'),'alert':'校园活动审核失败！该活动已审核','can':True})
    return render_with_type_(request,'Index/SchoolActivityIndex.html',{'projects':SchoolActivityRank.objects.filter(status = '通过'),'can':False})
#项目详情
def SchoolActivityDetail(request,id):
    try:  
        project = SchoolActivityRank.objects.get(id = int(id))
    except Exception,e: 
        return render_with_type_(request,'SchoolActivityDetail.html',{'alert':e})
    return render_with_type_(request,'SchoolActivityDetail.html',{'project':project})
#申请加入
def JoinSchoolActivity(request,id):
    alert = ''
    try:  
        project = SchoolActivityRank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
    except Exception,e:  
        return render_with_type_(request,'SchoolActivityDetail.html',{'alert':e})
    join = SchoolActivity(status = '待审核',StudentNum = student ,rankNum = project )
    join.save()
    alert = '成功加入！'
    return render_with_type_(request,'Index/SchoolActivityIndex.html',{'alert':alert})
#申请者的列表
def SchoolActivityIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = SchoolActivity.objects.filter(StudentNum= student)
    except Exception,e: 
        return render_with_type_(request,'index.html',{'activities':SchoolActivity.objects.filter(StudentNum = student),'alert':e})
    if request.user.has_perm('auth.is_instructor'):
        return render_with_type_(request,'Index/SchoolActivityIndex.html',{'projects':SchoolActivityRank.objects.filter(status = '待审核'),'can':True})
    return render_with_type_(request,'Index/SchoolActivityIndex.html',{'projects':SchoolActivityRank.objects.filter(status = '通过'),'can':False})
#管理申请的列表
def SchoolActivityList(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = SchoolActivityRank.objects.get(teacher = student)
        joins = SchoolActivity.objects.filter(rankNum = project)
    except Exception,e: 
        return render_with_type_(request,'SchoolActivityList.html',{'alert':e})
    return render_with_type_(request,'SchoolActivityList.html',{'projects':joins})
#申请者的详情
def SchoolActivitySDetail(request,id):
    try:  
        join = SchoolActivity.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type_(request,'SchoolActivitySDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        return render_with_type_(request,'SchoolActivitySDetail.html',{'project':join,'student':student})
    return render_with_type_(request,'SchoolActivitySDetail.html',{'alert':'您无权查看此报名信息！'})
#审核加入
def CheckSchoolActivityx(request,id,isok):
    try:  
        join = SchoolActivity.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_with_type_(request,'SchoolActivitySDetail.html',{'alert':e})
    if join.StudentNum.user == request.user:
        if isok:
            join.status = '通过'
        else:
            join.status = '未通过'
        join.save()
    return render_with_type_(request,'SchoolActivitySDetail.html',{'alert':'您无权审核此报名信息！'})
    
#我的项目
def index(request):
    alert = 'unlogin!'
    if request.user.is__authenticated():
        try:
            student = Students.objects.get(user = request.user)
            return render_with_type_(request,'index.html',{'projects':ResearchProject.objects.filter(StudentNum = student),
                                            'constructions':IdeologyConstruction.objects.filter(StudentNum = student),
                                            'lectures':Lecture.objects.filter(StudentNum = student),
                                            'volunteerings':Volunteering.objects.filter(StudentNum = student),
                                            'activities':SchoolActivity.objects.filter(StudentNum = student),
                                            'internships':Internship.objects.filter(StudentNum = student),
                                            'cadres':StudentCadreRank.objects.filter(StudentNum = student),
                                            'papers':PaperRank.objects.filter(StudentNum = student),
                                            'exchanges':ExchangeRank.objects.filter(StudentNum = student),
                                            'competitions':CompetitionRank.objects.filter(StudentNum = student)})
        except Exception,e:
            alert = 'unregister!'
    return render_with_type('/home',{'alert':alert})


#single model do not need index
'''
def PaperIndex(request):
    return render_with_type_(request,'Index/PaperIndex.html',{'projects':PaperRank.objects.filter(status = '通过')})

def CompetitionIndex(request):
    return render_with_type_(request,'Index/CompetitionIndex.html',{'projects':CompetitionRank.objects.filter(status = '通过')})

def ExchangeIndex(request):
    return render_with_type_(request,'Index/ExchangeIndex.html',{'projects':ExchangeRank.objects.filter(status = '通过')})

def StudentCadreIndex(request):
    return render_with_type_(request,'Index/StudentCadreIndex.html',{'projects':StudentCadreRank.objects.filter(status = '通过')})
'''
