# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from app.forms import CreateResearchProjectForm,CreatePaperForm,CreateCompetitionForm,CreateExchangeForm,CreateIdeologyConstructionForm,CreateLectureForm,CreateVolunteeringForm, CreateSchoolActivityForm,CreateInternshipForm,CreateStudentCadreForm
from app.forms import RegisterForm,ChangepwdForm,ChangeauthForm,ResetPasswordForm
from app.forms import ResearchProjectForm,IdeologyConstructionForm,LectureForm,VolunteeringForm,SchoolActivityForm,InternshipForm,StudentCadreForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect  
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from app.models import Students,Authorizations,Inspectors,ResearchProjectRank,PaperRank,CompetitionRank,ExchangeRank,IdeologyConstructionRank,LectureRank,VolunteeringRank,SchoolActivityRank,InternshipRank,StudentCadreRank,ResearchProject,IdeologyConstruction,Lecture,Volunteering,SchoolActivity,Internship,StudentCadre,statusChoice
import random,time
import uuid
import xlrd
import MySQLdb
'''import win32com.client as win32'''
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import DjangoWebProject.settings

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/index.html',
        {
            'title':'学生综合测评系统',
            'year':datetime.now().year,
        })

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })

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
"""def register(request):
     assert isinstance(request, HttpRequest)
     return render(
         request,
         'app/register.html',
         {'title':'register',
          'message':'add your message',
          'year':datetime.now().year,
          }
         )"""
         
def selecttype(request):
    usertypes = ['学生','老师','管理员']
    return render(request,'home.html',{'usertypes':usertypes})

def search_form(request):
    return render_to_response('search_form.html')

def search(request):
    if 'q' in request.GET:#GET是一个dict，使用文本框的name作为key
    #在这里需要做一个判断，是否存在提交数据，以免报错
        q = request.GET['q']
        #使用lookup后缀，意思为书名不区分大小写，包含q就可以
        users = User.objects.filter(username__icontains=q)
        return render_to_response('search_results.html', {'users' : users, 'query':q})
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
            user = User.objects.filter(username=cd['username'],email=cd['email'])
            if user is not None:
                user.update(password=make_password(cd['password']))
                return HttpResponseRedirect('/login')
    else:
        form = ResetPasswordForm()
    return render_to_response('reset_form.html', {'form': form})

def changepassword(request,username):
	error = []
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
	return render_to_response('changepassword.html',{'form':form,'error':error})

def changeauth(request,username):
	error = []
	if request.method == 'POST':
		form = ChangeauthForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			nowuser = request.user
			if nowuser is not None:
				if nowuser.is_superuser:
				    user = User.objects.get(username__exact=username)
				    auth = Students.objects.get(user__exact=user.id).auth
				    auth.isTeacher = data['isTeacher']
				    auth.research = data['research']
				    auth.paper = data['paper']
				    auth.competition = data['competition']
				    auth.exchange = data['exchange']
				    auth.ideologyConstruction = data['ideologyConstruction']
				    auth.lecture = data['lecture']
				    auth.volunteering = data['volunteering']
				    auth.schoolActivity= data['schoolActivity']
				    auth.internship = data['internship']
				    auth.studentCadre = data['studentCadre']
				    auth.save()
				    return HttpResponseRedirect('/admin/app/students')
				else:
				    error.append('错误的请求：管理员身份验证未通过')
			else:
				error.append('错误的请求：请先登录')
		else:
			error.append('Please input the required domain')
	else:
		form = ChangeauthForm()
	return render_to_response('changeauth.html',{'form':form,'error':error,'username':username})


def createPaper(request):
    error = []
    if request.method == 'POST':
        form = CreatePaperForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = PaperRank(rankName = cd['ProjectName'],
                                journalName = cd['JournalName'],
                                student = Students.objects.get(user = request.user),
                                startingTime = cd['ProjectTime'],
                                status = '待审核',
                                Level = '',
                                AuthorRanking = 0,
                                score = 0,
                                CompleteNum = 0,
                                inspector = Inspectors.objects.get(inspector = 10002))
            if True:
                project.save()
                return HttpResponse('论文申请已提交！')
            else:
                error.append('Please check your importation')
        else:
            error.append('Please input information of your project')
    else:
        form = CreatePaperForm()
    return render_to_response('createPaper.html',{'form':form,'error':error})
def createCompetition(request):
    error = []
    if request.method == 'POST':
        form = CreateCompetitionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = CompetitionRank(rankName = cd['ProjectName'],
                                student = Students.objects.get(user = request.user),
                                startingTime = cd['ProjectTime'],
                                status = '待审核',
                                rank = '0',
                                Level = '',
                                score = 0,
                                CompleteNum = 0,
                                inspector = Inspectors.objects.get(number = 10001))
            if True:
                project.save()
                return HttpResponse('竞赛申请已提交！')
            else:
                error.append('Please check your importation')
        else:
            error.append('Please input information of your project')
    else:
        form = CreateCompetitionForm()
    return render_to_response('createCompetition.html',{'form':form,'error':error})
def createStudentCadre(request):
    error = []
    if request.method == 'POST':
        form = CreateStudentCadreForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = StudentCadreRank(teacher = Students.objects.get(user = request.user),
                                organizitionType = cd['organizitionType'],
                                organizitionName = cd['organizitionName'],
                                status = '待审核',
                                score = 0,
                                CompleteNum = 0,
                                inspector = Inspectors.objects.get(number = 10002))
            if True:
                project.save()
                return HttpResponse('学生干部信息申请已提交！')
            else:
                error.append('Please check your importation')
        else:
            error.append('Please input information of your project')
    else:
        form = CreateStudentCadreForm()
    return render_to_response('createStudentCadre.html',{'form':form,'error':error})
def createExchange(request):
    error = []
    if request.method == 'POST':
        form = CreateExchangeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = ExchangeRank(rankName = cd['ProjectName'],
                                type = cd['type'],
                                nature = cd['nature'],
                                student = Students.objects.get(user = request.user),
                                startTime = cd['startTime'],
                                endTime = cd['endTime'],
                                status = '待审核',
                                score = 0,
                                CompleteNum = 0,
                                inspector = Inspectors.objects.get(number = 10001))
            if True:
                project.save()
                return HttpResponse('交流交换申请已提交！')
            else:
                error.append('Please check your importation')
        else:
            error.append('Please input information of your project')
    else:
        form = CreateExchangeForm()
    return render_to_response('createExchange.html',{'form':form,'error':error})


def createResearchProject(request):
    error = []
    alert = ''
    if request.method == 'POST':
        form = CreateResearchProjectForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = ResearchProjectRank(rankName = cd['ProjectName'],teacher = Students.objects.get(user = request.user),startingTime = cd['ProjectTime'],status = '待审核',rank = '',ManagerScore = 0,MemberScore = 0,CompleteNum = 0,inspector = Inspectors.objects.get(number = 10002))
            if True:
                project.save()
                alert = '成功创建！'
            else:
                error.append('Please check your importation')
        else:
            error.append('Please input information of your project')
    else:
        form = CreateResearchProjectForm()
    return render_to_response('createResearchProject.html',{'form':form,'error':error,'alert':alert})


def researchProject(request,id):
    error = []
    try:  
        project = ResearchProjectRank.objects.get(id = int(id))
        auth = Students.objects.get(user = request.user).auth
        inspector = Inspectors.objects.get(user = request.user)
    except Exception,e:  
        error.append(e)
        return render_to_response('ResearchProject.html',{'error':error})
    if project.status == '待审核':
        if request.method == 'POST':
            form = ResearchProjectForm(request.POST)
            if form.is_valid() and auth.isTeacher and auth.research:
                cd = form.cleaned_data
                try:
                    project.rank = cd['rank']
                    project.MemberScore = cd['MemberScore']
                    project.ManagerScore = cd['ManagerScore']
                    project.status = cd['status']
                    project.inspector = inspector 
                    project.save()
                    return render_to_response('ResearchProjectIndex.html',{'projects':ResearchProjectRank.objects.filter(status = '待审核'),'alert':'科研立项审核成功！','can':True})
                except Exception,e:  
                    error.append('Please check your importation')
            else:
                error.append('Please input information of your project')
        else:
            form = ResearchProjectForm()
        return render_to_response('ResearchProject.html',{'form':form,'project':project,'error':error})
    elif auth.isTeacher and auth.ideologyConstruction:
       return render_to_response('ResearchProjectIndex.html',{'projects':ResearchProjectRank.objects.filter(status = '待审核'),'alert':'科研立项审核失败！该活动已审核','can':True})
    return render_to_response('ResearchProjectIndex.html',{'projects':ResearchProjectRank.objects.filter(status = '通过'),'alert':'','can':False})


def ResearchProjectDetail(request,id):
    try:  
        project = ResearchProjectRank.objects.get(id = int(id))
    except Exception,e: 
        return render_to_response('ResearchProjectDetail.html',{'error':e})
    return render_to_response('ResearchProjectDetail.html',{'project':project})


def JoinResearchProject(request,id):
    alert = ''
    try:  
        project = ResearchProjectRank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
    except Exception,e:  
        return render_to_response('ResearchProjectDetail.html',{'error':e})
    join = ResearchProject(status = '待审核',StudentNum = student ,rankNum = project , inspector = Inspectors.objects.get(number = 10002))
    join.save()
    alert = '成功加入！'
    return render_to_response('ResearchProjectIndex.html',{'alert':alert})


def ResearchProjectList(request):
    try: 
        student = Students.objects.get(user = request.user)
        project = ResearchProjectRank.objects.get(teacher = student)
        joins = ResearchProject.objects.filter(rankNum = project)
    except Exception,e: 
        return render_to_response('ResearchProjectList.html',{'error':e,'alert':''})
    return render_to_response('ResearchProjectList.html',{'projects':joins,'alert':''})
    

def ResearchProjectSDetail(request,id):
    try:  
        join = ResearchProject.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_to_response('ResearchProjectSDetail.html',{'error':e})
    if join.StudentNum.user == request.user:
        return render_to_response('ResearchProjectSDetail.html',{'project':join,'student':student})
    return render_to_response('ResearchProjectSDetail.html',{'error':'您无权查看此报名信息！'})


def CheckResearchProject(request,id,isok):
    try:  
        join = ResearchProject.objects.get(id = int(id))
        student = join.StudentNum
    except Exception,e: 
        return render_to_response('ResearchProjectSDetail.html',{'error':e})
    if join.StudentNum.user == request.user:
        if isok:
            join.status = '通过'
        else:
            join.status = '未通过'
        join.save()
    return render_to_response('ResearchProjectSDetail.html',{'error':'您无权审核此报名信息！'})



def createIdeologyConstruction(request):
    error = []
    if request.method == 'POST':
        form = CreateIdeologyConstructionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = IdeologyConstructionRank(rankName = cd['ProjectName'],
                                type = cd['type'],
                                teacher = Students.objects.get(user = request.user),
                                startingTime = cd['startingTime'],
                                organizer = cd['organizer'],
                                Location = cd['Location'],
                                Content = cd['Content'],
                                status = '待审核',
                                score = 0,
                                CompleteNum = 0,
                                inspector = Inspectors.objects.get(number = 10002))
            if True:
                project.save()
                return HttpResponse('思建活动申请已提交！')
            else:
                error.append('Please check your importation')
        else:
            error.append('Please input information of your project')
    else:
        form = CreateIdeologyConstructionForm()
    return render_to_response('createIdeologyConstruction.html',{'form':form,'error':error})


def ideologyConstruction(request,id):
    error = []
    try:  
        project = IdeologyConstructionRank.objects.get(id = int(id))
        auth = Students.objects.get(user = request.user).auth
        inspector = Inspectors.objects.get(user = request.user)
    except Exception,e:  
        error.append(e)
        return render_to_response('IdeologyConstruction.html',{'error':error})
    if project.status == '未通过':
        if request.method == 'POST':
            form = IdeologyConstructionForm(request.POST)
            if form.is_valid() and auth.isTeacher and auth.ideologyConstruction:
                cd = form.cleaned_data
                try:
                    project.score = cd['score']
                    project.status = cd['status']
                    project.inspector = inspector
                    project.save()
                    return render_to_response('IdeologyConstructionIndex.html',{'projects':IdeologyConstructionRank.objects.filter(status = '待审核'),'alert':'思建活动审核成功！','can':True})
                except Exception,e:  
                    error.append('Please check your importation')
            else:
                error.append('Please input information of your project')
        else:
            form = IdeologyConstructionForm()
            return render_to_response('IdeologyConstruction.html',{'form':form,'project':project,'error':error})
    elif auth.isTeacher and auth.ideologyConstruction:
       return render_to_response('IdeologyConstructionIndex.html',{'projects':IdeologyConstructionRank.objects.filter(status = '待审核'),'alert':'思建活动审核失败！该活动已审核','can':True})
    return render_to_response('IdeologyConstructionIndex.html',{'projects':IdeologyConstructionRank.objects.filter(status = '通过'),'alert':'','can':False})


def IdeologyConstructionDetail(request,id):
    try:  
        project = IdeologyConstructionRank.objects.get(id = int(id))
    except Exception,e: 
        return render_to_response('IdeologyConstructionDetail.html',{'error':e})
    return render_to_response('IdeologyConstructionDetail.html',{'project':project})


def JoinIdeologyConstruction(request,id):
    alert = ''
    try:  
        project = IdeologyConstructionRank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
    except Exception,e:  
        return render_to_response('IdeologyConstructionDetail.html',{'error':e})
    join = IdeologyConstruction(status = '待审核',StudentNum = student ,rankNum = project , inspector = Inspectors.objects.get(number = 10002))
    join.save()
    alert = '成功加入！'
    return render_to_response('IdeologyConstructionIndex.html',{'alert':alert})


def createLecture(request):
    error = []
    if request.method == 'POST':
        form = CreateLectureForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = LectureRank(rankName = cd['ProjectName'],
                                type = cd['type'],
                                teacher = Students.objects.get(user = request.user),
                                startingTime = cd['startingTime'],
                                organizer = cd['organizer'],
                                speaker = cd['speaker'],
                                Location = cd['Location'],
                                Content = cd['Content'],
                                status = '待审核',
                                score = 0,
                                CompleteNum = 0,
                                inspector = Inspectors.objects.get(number = 10002))
            if True:
                project.save()
                return HttpResponse('讲座活动申请已提交！')
            else:
                error.append('Please check your importation')
        else:
            error.append('Please input information of your project')
    else:
        form = CreateLectureForm()
    return render_to_response('createLecture.html',{'form':form,'error':error})


def lecture(request,id):
    error = []
    try:  
        project = LectureRank.objects.get(id = int(id))
        auth = Students.objects.get(user = request.user).auth
        inspector = Inspectors.objects.get(user = request.user)
    except Exception,e:  
        error.append(e)
        return render_to_response('IdeologyConstruction.html',{'error':error})
    if project.status == '待审核':
        if request.method == 'POST':
            form = LectureForm(request.POST)
            if form.is_valid() and auth.isTeacher and auth.lecture:
                cd = form.cleaned_data
                try:
                    project.score = cd['score']
                    project.status = cd['status']
                    project.inspector = inspector
                    project.save()
                    return render_to_response('LectureIndex.html',{'projects':LectureRank.objects.filter(status = '待审核'),'alert':'讲座活动审核成功！','can':True})
                except Exception,e:  
                    error.append('Please check your importation')
            else:
                error.append('Please input information of your project')
        else:
            form = LectureForm()
            return render_to_response('Lecture.html',{'form':form,'project':project,'error':error})
    elif auth.isTeacher and auth.lecture:
       return render_to_response('LectureIndex.html',{'projects':LectureRank.objects.filter(status = '待审核'),'alert':'讲座活动审核失败！该活动已审核','can':True})
    return render_to_response('LectureIndex.html',{'projects':LectureRank.objects.filter(status = '通过'),'alert':'','can':False})


def LectureDetail(request,id):
    try:  
        project = LectureRank.objects.get(id = int(id))
    except Exception,e: 
        return render_to_response('LectureDetail.html',{'error':e})
    return render_to_response('LectureDetail.html',{'project':project})


def JoinLecture(request,id):
    alert = ''
    try:  
        project = LectureRank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
    except Exception,e:  
        return render_to_response('LectureDetail.html',{'error':e})
    join = Lecture(status = '待审核',StudentNum = student ,rankNum = project , inspector = Inspectors.objects.get(number = 10002))
    join.save()
    alert = '成功加入！'
    return render_to_response('LectureIndex.html',{'alert':alert})


def createVolunteering(request):
    error = []
    if request.method == 'POST':
        form = CreateVolunteeringForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = VolunteeringRank(rankName = cd['ProjectName'],
                                teacher = Students.objects.get(user = request.user),
                                startingTime = cd['startingTime'],
                                volunteerTime = cd['volunteerTime'],
                                organizer = cd['organizer'],
                                Location = cd['Location'],
                                Content = cd['Content'],
                                status = '待审核',
                                score = 0,
                                CompleteNum = 0,
                                inspector = Inspectors.objects.get(number = 10002))
            if True:
                project.save()
                return HttpResponse('志愿活动申请已提交！')
            else:
                error.append('Please check your importation')
        else:
            error.append('Please input information of your project')
    else:
        form = CreateVolunteeringForm()
    return render_to_response('createVolunteering.html',{'form':form,'error':error})


def volunteering(request,id):
    error = []
    try:  
        project = VolunteeringRank.objects.get(id = int(id))
        auth = Students.objects.get(user = request.user).auth
        inspector = Inspectors.objects.get(user = request.user)
    except Exception,e:  
        error.append(e)
        return render_to_response('Volunteering.html',{'error':error})
    if project.status == '待审核':
        if request.method == 'POST':
            form = VolunteeringForm(request.POST)
            if form.is_valid() and auth.isTeacher and auth.volunteering:
                cd = form.cleaned_data
                try:
                    project.score = cd['score']
                    project.status = cd['status']
                    project.inspector = inspector
                    project.save()
                    return render_to_response('VolunteeringIndex.html',{'projects':VolunteeringRank.objects.filter(status = '待审核'),'alert':'志愿活动审核成功！','can':True})
                except Exception,e:  
                    error.append('Please check your importation')
            else:
                error.append('Please input information of your project')
        else:
            form = VolunteeringForm()
            return render_to_response('Lecture.html',{'form':form,'project':project,'error':error})
    elif auth.isTeacher and auth.volunteering:
       return render_to_response('VolunteeringIndex.html',{'projects':VolunteeringRank.objects.filter(status = '待审核'),'alert':'志愿活动审核失败！该活动已审核','can':True})
    return render_to_response('VolunteeringIndex.html',{'projects':VolunteeringRank.objects.filter(status = '通过'),'alert':'','can':False})


def VolunteeringDetail(request,id):
    try:  
        project = VolunteeringRank.objects.get(id = int(id))
    except Exception,e: 
        return render_to_response('VolunteeringDetail.html',{'error':e})
    return render_to_response('VolunteeringDetail.html',{'project':project})


def JoinVolunteering(request,id):
    alert = ''
    try:  
        project = VolunteeringRank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
    except Exception,e:  
        return render_to_response('VolunteeringDetail.html',{'error':e})
    join = Volunteering(status = '待审核',StudentNum = student ,rankNum = project , inspector = Inspectors.objects.get(number = 10002))
    join.save()
    alert = '成功加入！'
    return render_to_response('VolunteeringIndex.html',{'alert':alert})


def createSchoolActivity(request):
    error = []
    if request.method == 'POST':
        form = CreateSchoolActivityForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = SchoolActivityRank(rankName = cd['ProjectName'],
                                teacher = Students.objects.get(user = request.user),
                                startingTime = cd['startingTime'],
                                type = cd['type'],
                                sponsor = cd['sponsor'],
                                organizer = cd['organizer'],
                                awardLevel = cd['awardLevel'],
                                status = '待审核',
                                score = 0,
                                CompleteNum = 0,
                                inspector = Inspectors.objects.get(number = 10002))
            if True:
                project.save()
                return HttpResponse('校园活动申请已提交！')
            else:
                error.append('Please check your importation')
        else:
            error.append('Please input information of your project')
    else:
        form = CreateSchoolActivityForm()
    return render_to_response('createSchoolActivity.html',{'form':form,'error':error})


def schoolActivity(request,id):
    error = []
    try:  
        project = SchoolActivityRank.objects.get(id = int(id))
        auth = Students.objects.get(user = request.user).auth
        inspector = Inspectors.objects.get(user = request.user)
    except Exception,e:  
        error.append(e)
        return render_to_response('SchoolActivity.html',{'error':error})
    if project.status == '待审核':
        if request.method == 'POST':
            form = SchoolActivityForm(request.POST)
            if form.is_valid() and auth.isTeacher and auth.schoolActivity:
                cd = form.cleaned_data
                try:
                    project.score = cd['score']
                    project.status = cd['status']
                    project.inspector = inspector
                    project.save()
                    return render_to_response('SchoolActivityIndex.html',{'projects':SchoolActivityRank.objects.filter(status = '待审核'),'alert':'校园活动审核成功！','can':True})
                except Exception,e:  
                    error.append('Please check your importation')
            else:
                error.append('Please input information of your project')
        else:
            form = SchoolActivityForm()
            return render_to_response('Lecture.html',{'form':form,'project':project,'error':error})
    elif auth.isTeacher and auth.schoolActivity:
       return render_to_response('SchoolActivityIndex.html',{'projects':SchoolActivityRank.objects.filter(status = '待审核'),'alert':'校园活动审核失败！该活动已审核','can':True})
    return render_to_response('SchoolActivityIndex.html',{'projects':SchoolActivityRank.objects.filter(status = '通过'),'alert':'','can':False})


def SchoolActivityDetail(request,id):
    try:  
        project = SchoolActivityRank.objects.get(id = int(id))
    except Exception,e: 
        return render_to_response('SchoolActivityDetail.html',{'error':e})
    return render_to_response('SchoolActivityDetail.html',{'project':project})


def JoinSchoolActivity(request,id):
    alert = ''
    try:  
        project = SchoolActivityRank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
    except Exception,e:  
        return render_to_response('SchoolActivityDetail.html',{'error':e})
    join = SchoolActivity(status = '待审核',StudentNum = student ,rankNum = project , inspector = Inspectors.objects.get(number = 10002))
    join.save()
    alert = '成功加入！'
    return render_to_response('SchoolActivityIndex.html',{'alert':alert})


def createInternship(request):
    error = []
    if request.method == 'POST':
        form = CreateInternshipForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = InternshipRank(rankName = cd['ProjectName'],
                                teacher = Students.objects.get(user = request.user),
                                InternshipTime = cd['startingTime'],
                                type = cd['type'],
                                status = '待审核',
                                score = 0,
                                CompleteNum = 0,
                                inspector = Inspectors.objects.get(number = 10002))
            if True:
                project.save()
                return HttpResponse('实践实习信息申请已提交！')
            else:
                error.append('Please check your importation')
        else:
            error.append('Please input information of your project')
    else:
        form = CreateInternshipForm()
    return render_to_response('createInternship.html',{'form':form,'error':error})


def internship(request,id):
    error = []
    try:  
        project = InternshipRank.objects.get(id = int(id))
        auth = Students.objects.get(user = request.user).auth
        inspector = Inspectors.objects.get(user = request.user)
    except Exception,e:  
        error.append(e)
        return render_to_response('Internship.html',{'error':error})
    if project.status == '待审核':
        if request.method == 'POST':
            form = InternshipForm(request.POST)
            if form.is_valid() and auth.isTeacher and auth.internship:
                cd = form.cleaned_data
                try:
                    project.score = cd['score']
                    project.status = cd['status']
                    project.inspector = inspector
                    project.save()
                    return render_to_response('InternshipIndex.html',{'projects':InternshipRank.objects.filter(status = '待审核'),'alert':'实践实习审核成功！','can':True})
                except Exception,e:  
                    error.append('Please check your importation')
            else:
                error.append('Please input information of your project')
        else:
            form = InternshipForm()
            return render_to_response('Lecture.html',{'form':form,'project':project,'error':error})
    elif auth.isTeacher and auth.internship:
       return render_to_response('InternshipIndex.html',{'projects':InternshipRank.objects.filter(status = '待审核'),'alert':'实践实习审核失败！该活动已审核','can':True})
    return render_to_response('InternshipIndex.html',{'projects':InternshipRank.objects.filter(status = '通过'),'alert':'','can':False})


def InternshipDetail(request,id):
    try:  
        project = InternshipRank.objects.get(id = int(id))
    except Exception,e: 
        return render_to_response('InternshipDetail.html',{'error':e})
    return render_to_response('InternshipDetail.html',{'project':project})


def JoinInternship(request,id):
    alert = ''
    try:  
        project = InternshipRank.objects.get(id = int(id))
        student = Students.objects.get(user = request.user)
    except Exception,e:  
        return render_to_response('InternshipDetail.html',{'error':e})
    join = Internship(status = '待审核',StudentNum = student ,rankNum = project , inspector = Inspectors.objects.get(number = 10002))
    join.save()
    alert = '成功加入！'
    return render_to_response('InternshipIndex.html',{'alert':alert})


def Excel(request):
    Inspector = Inspectors.objects.get(user = request.user)
    book = xlrd.open_workbook('D:\\test.xls')
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
          Speciality     = sheet.cell(r,14).value
          Province       = sheet.cell(r,15).value
          theuser = User(username = studentNum,password = make_password('uibe'+IdentityNumber[-6:]),email = Email)
          theuser.save()
          theauth = Authorizations(id = uuid.uuid1(),
                                   isTeacher = False,
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
                             root =Root,nation =Nation,
                             politicalStatus =PoliticalStatus,
                             location =Location,
                             identityType =IdentityType,
                             identityNumber =int(IdentityNumber),
                             speciality =Speciality,
                             province =Province,
                             inspector =Inspector,
                             collegeEntranceExaminationScore =CollegeEntranceExaminationScore)
          student.save()
    return HttpResponseRedirect('/')

def index(request):
    student = Students.objects.get(user = request.user)
    return render_to_response('index.html',{'projects':ResearchProject.objects.filter(StudentNum = student),
                                            'constructions':IdeologyConstruction.objects.filter(StudentNum = student),
                                            'lectures':Lecture.objects.filter(StudentNum = student),
                                            'volunteerings':Volunteering.objects.filter(StudentNum = student),
                                            'activities':SchoolActivity.objects.filter(StudentNum = student),
                                            'internships':Internship.objects.filter(StudentNum = student),
                                            'cadres':StudentCadre.objects.filter(StudentNum = student)})


def ResearchProjectIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = ResearchProject.objects.filter(StudentNum= student)
    except Exception,e: 
        return render_to_response('index.html',{'projects':ResearchProject.objects.filter(StudentNum = student),'alert':e})
    if student.auth.isTeacher and student.auth.research:
        return render_to_response('researchProjectIndex.html',{'projects':ResearchProjectRank.objects.filter(status = '待审核'),'alert':'','can':True})
    if project.count() == 0:
        return render_to_response('researchProjectIndex.html',{'projects':ResearchProjectRank.objects.filter(status = '通过'),'alert':'','can':False})
    return render_to_response('index.html',{'projects':ResearchProject.objects.filter(StudentNum = student),'alert':'您已加入科研立项!'})


#single model do not need index
'''
def PaperIndex(request):
    return render_to_response('PaperIndex.html',{'projects':PaperRank.objects.filter(status = '通过')})

def CompetitionIndex(request):
    return render_to_response('CompetitionIndex.html',{'projects':CompetitionRank.objects.filter(status = '通过')})

def ExchangeIndex(request):
    return render_to_response('ExchangeIndex.html',{'projects':ExchangeRank.objects.filter(status = '通过')})

def StudentCadreIndex(request):
    return render_to_response('StudentCadreIndex.html',{'projects':StudentCadreRank.objects.filter(status = '通过')})
'''


def IdeologyConstructionIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = IdeologyConstruction.objects.filter(StudentNum= student)
    except Exception,e: 
        return render_to_response('index.html',{'constructions':IdeologyConstruction.objects.filter(StudentNum = student),'alert':e})
    if student.auth.isTeacher and student.auth.ideologyConstruction:
        return render_to_response('IdeologyConstructionIndex.html',{'projects':IdeologyConstructionRank.objects.filter(status = '待审核'),'alert':'','can':True})
    return render_to_response('IdeologyConstructionIndex.html',{'projects':IdeologyConstructionRank.objects.filter(status = '通过'),'alert':'','can':False})


def LectureIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = Lecture.objects.filter(StudentNum= student)
    except Exception,e: 
        return render_to_response('index.html',{'lectures':Lecture.objects.filter(StudentNum = student),'alert':e})
    if student.auth.isTeacher and student.auth.lecture:
        return render_to_response('LectureIndex.html',{'projects':LectureRank.objects.filter(status = '待审核'),'alert':'','can':True})
    return render_to_response('LectureIndex.html',{'projects':LectureRank.objects.filter(status = '通过'),'alert':'','can':False})


def VolunteeringIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = Volunteering.objects.filter(StudentNum= student)
    except Exception,e: 
        return render_to_response('index.html',{'volunteerings':Volunteering.objects.filter(StudentNum = student),'alert':e})
    if student.auth.isTeacher and student.auth.ideologyConstruction:
        return render_to_response('VolunteeringIndex.html',{'projects':VolunteeringRank.objects.filter(status = '待审核'),'alert':'','can':True})
    return render_to_response('VolunteeringIndex.html',{'projects':VolunteeringRank.objects.filter(status = '通过'),'alert':'','can':False})


def SchoolActivityIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = SchoolActivity.objects.filter(StudentNum= student)
    except Exception,e: 
        return render_to_response('index.html',{'activities':SchoolActivity.objects.filter(StudentNum = student),'alert':e})
    if student.auth.isTeacher and student.auth.ideologyConstruction:
        return render_to_response('SchoolActivityIndex.html',{'projects':SchoolActivityRank.objects.filter(status = '待审核'),'alert':'','can':True})
    return render_to_response('SchoolActivityIndex.html',{'projects':SchoolActivityRank.objects.filter(status = '通过'),'alert':'','can':False})


def InternshipIndex(request):
    try:  
        student = Students.objects.get(user = request.user)
        project = Internship.objects.filter(StudentNum= student)
    except Exception,e: 
        return render_to_response('index.html',{'internships':Internship.objects.filter(StudentNum = student),'alert':e})
    if student.auth.isTeacher and student.auth.ideologyConstruction:
        return render_to_response('InternshipIndex.html',{'projects':InternshipRank.objects.filter(status = '待审核'),'alert':'','can':True})
    return render_to_response('InternshipIndex.html',{'projects':InternshipRank.objects.filter(status = '通过'),'alert':'','can':False})