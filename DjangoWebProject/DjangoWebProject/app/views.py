# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from app.forms import ResetPasswordForm
from app.forms import CreateResearchProjectForm,CreatePaperForm,CreateCompetitionForm,CreateExchangeForm,CreateIdeologyConstructionForm,CreateLectureForm,CreateVolunteeringForm, CreateSchoolActivityForm,CreateInternshipForm,CreateStudentCadreForm,ResearchProjectForm
from app.forms import RegisterForm,ChangepwdForm,ChangeauthForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect  
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from app.models import Students,Authorizations,Inspectors,ResearchProjectRank,PaperRank,CompetitionRank,ExchangeRank,IdeologyConstructionRank,LectureRank,VolunteeringRank,SchoolActivityRank,InternshipRank,StudentCadreRank
import random,time
'''import xlrd'''
import MySQLdb
'''import win32com.client as win32'''

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/index.html',
        {
            'title':'SITE',
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

"""cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                ['siteowner@example.com'],
            )"""

def createResearchProject(request):
    error = []
    if request.method == 'POST':
        form = CreateResearchProjectForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = ResearchProjectRank(rankName = cd['ProjectName'],teacherNum = Students.objects.get(user = request.user),startingTime = cd['ProjectTime'],status = 1,rank = '',ManagerScore = 0,MemberScore = 0,CompleteNum = 0,inspectorNum = Inspectors.objects.get(inspectorNum = 10002))
            if True:
                project.save()
                return HttpResponse('科研立项项目创建成功！')
            else:
                error.append('Please check your importation')
        else:
            error.append('Please input information of your project')
    else:
        form = CreateResearchProjectForm()
    return render_to_response('createResearchProject.html',{'form':form,'error':error})

def ResearchProject(request,id):
    error = []
    try:  
        project = ResearchProjectRank.objects.get(id = int(id))
        auth = Students.objects.get(user = request.user).auth
    except Exception,e:  
        error.append(e)
    if request.method == 'POST':
        form = ResearchProjectForm(request.POST)
        if form.is_valid() and auth.isTeacher:
            cd = form.cleaned_data
            try:
                project.rank = cd['rank']
                project.MemberScore = cd['MemberScore']
                project.ManagerScore = cd['ManagerScore']
                project.status = cd['status']
                project.inspectorNum = Inspectors.objects.get(user = request.user)
                project.save()
                return HttpResponse('科研立项项目审核成功！')
            except Exception,e:  
                error.append('Please check your importation')
        else:
            error.append('Please input information of your project')
    else:
        form = ResearchProjectForm()
    return render_to_response('ResearchProject.html',{'form':form,'project':project,'error':error})

def createPaper(request):
    error = []
    if request.method == 'POST':
        form = CreatePaperForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = PaperRank(rankName = cd['ProjectName'],
                                journalName = cd['JournalName'],
                                teacherNum = Students.objects.get(user = request.user),
                                startingTime = cd['ProjectTime'],
                                status = 1,
                                Level = '',
                                AuthorRanking = 0,
                                score = 0,
                                CompleteNum = 0,
                                inspectorNum = Inspectors.objects.get(inspectorNum = 10002))
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
                                teacherNum = Students.objects.get(user = request.user),
                                startingTime = cd['ProjectTime'],
                                status = 1,
                                rank = '',
                                Level = '',
                                score = 0,
                                CompleteNum = 0,
                                inspectorNum = Inspectors.objects.get(inspectorNum = 10002))
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

def createExchange(request):
    error = []
    if request.method == 'POST':
        form = CreateExchangeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = ExchangeRank(rankName = cd['ProjectName'],
                                type = cd['type'],
                                nature = cd['nature'],
                                teacherNum = Students.objects.get(user = request.user),
                                startTime = cd['startTime'],
                                endTime = cd['endTime'],
                                status = 1,
                                score = 0,
                                CompleteNum = 0,
                                inspectorNum = Inspectors.objects.get(inspectorNum = 10002))
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

def createIdeologyConstruction(request):
    error = []
    if request.method == 'POST':
        form = CreateIdeologyConstructionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = IdeologyConstructionRank(rankName = cd['ProjectName'],
                                type = cd['type'],
                                teacherNum = Students.objects.get(user = request.user),
                                startingTime = cd['startingTime'],
                                organizer = cd['organizer'],
                                Location = cd['Location'],
                                Content = cd['Content'],
                                status = 1,
                                score = 0,
                                CompleteNum = 0,
                                inspectorNum = Inspectors.objects.get(inspectorNum = 10002))
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

def createLecture(request):
    error = []
    if request.method == 'POST':
        form = CreateLectureForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = LectureRank(rankName = cd['ProjectName'],
                                type = cd['type'],
                                teacherNum = Students.objects.get(user = request.user),
                                startingTime = cd['startingTime'],
                                organizer = cd['organizer'],
                                speaker = cd['speaker'],
                                Location = cd['Location'],
                                Content = cd['Content'],
                                status = 1,
                                score = 0,
                                CompleteNum = 0,
                                inspectorNum = Inspectors.objects.get(inspectorNum = 10002))
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

def createVolunteering(request):
    error = []
    if request.method == 'POST':
        form = CreateVolunteeringForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = VolunteeringRank(rankName = cd['ProjectName'],
                                teacherNum = Students.objects.get(user = request.user),
                                startingTime = cd['startingTime'],
                                volunteerTime = cd['volunteerTime'],
                                organizer = cd['organizer'],
                                Location = cd['Location'],
                                Content = cd['Content'],
                                status = 1,
                                score = 0,
                                CompleteNum = 0,
                                inspectorNum = Inspectors.objects.get(inspectorNum = 10002))
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

def createSchoolActivity(request):
    error = []
    if request.method == 'POST':
        form = CreateSchoolActivityForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = SchoolActivityRank(rankName = cd['ProjectName'],
                                teacherNum = Students.objects.get(user = request.user),
                                startingTime = cd['startingTime'],
                                type = cd['type'],
                                sponsor = cd['sponsor'],
                                organizer = cd['organizer'],
                                awardLevel = cd['awardLevel'],
                                status = 1,
                                score = 0,
                                CompleteNum = 0,
                                inspectorNum = Inspectors.objects.get(inspectorNum = 10002))
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

def createInternship(request):
    error = []
    if request.method == 'POST':
        form = CreateInternshipForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = InternshipRank(rankName = cd['ProjectName'],
                                teacherNum = Students.objects.get(user = request.user),
                                startingTime = cd['startingTime'],
                                type = cd['type'],
                                status = 1,
                                score = 0,
                                CompleteNum = 0,
                                inspectorNum = Inspectors.objects.get(inspectorNum = 10002))
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

def createStudentCadre(request):
    error = []
    if request.method == 'POST':
        form = CreateStudentCadreForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            project = StudentCadreRank(teacherNum = Students.objects.get(user = request.user),
                                organizitionType = cd['organizitionType'],
                                organizitionName = cd['organizitionName'],
                                status = 1,
                                score = 0,
                                CompleteNum = 0,
                                inspectorNum = Inspectors.objects.get(inspectorNum = 10002))
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


'''#excel 批量添加数据到数据库
def ExcelToMysql(request):
    book = xlrd.open_workbook('excel文件路径')
    sheet = book.sheet_by_name('excel工作簿名')

    #建立一个MySQL连接
    database = MySQLdb.connect (host="服务器名", user = "root", passwd = "", db = "数据库名")

    # 获得游标对象, 用于逐行遍历数据库数据
    cursor = database.cursor()

    # 创建插入SQL语句
    query = "INSERT INTO 目标数据库表 VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'')"
    # 创建一个for循环迭代读取xls文件每行数据的, 从第二行开始是要跳过标题
    for r in range(1, sheet.nrows):
          user      = sheet.cell(r,0).value
          StudentNum = sheet.cell(r,1).value
          name          = sheet.cell(r,2).value
          sex     = sheet.cell(r,3).value
          year       = sheet.cell(r,4).value
          phone = sheet.cell(r,5).value
          email        = sheet.cell(r,6).value
          born       = sheet.cell(r,7).value
          root     = sheet.cell(r,8).value
          nation        = sheet.cell(r,9).value
          politicalStatus      = sheet.cell(r,10).value
          location          = sheet.cell(r,11).value
          identityType   = sheet.cell(r,12).value
          identityNumber = sheet.cell(r,13).value
          speciality         = sheet.cell(r,14).value
          province       = sheet.cell(r,15).value
          collegeEntranceExaminationScore   = sheet.cell(r,16).value

          values = (user,StudentNum,name,sex,year,phone,email,born,root,nation,politicalStatus,location,identityType,identityNumber,speciality,province,collegeEntranceExaminationScore)

          # 执行sql语句
          cursor.execute(query, values)

    # 关闭游标
    cursor.close()

    # 提交
    database.commit()

    # 关闭数据库连接
    database.close()

    # 打印结果
    print ""
    print "Done! "
    print ""
    print u"我刚导入了数据到MySQL!"
    '''