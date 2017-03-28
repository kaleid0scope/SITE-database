from app.models import *
from django.contrib.auth.models import User

def GetComplete(request,student):
    list = clean(student.complete)
    list = GetCompleteTeam(ResearchProject.objects.filter(StudentNum = student),list,student)
    list = GetCompleteProject(IdeologyConstruction.objects.filter(StudentNum = student),IdeologyConstructionRank.objects.filter(teacher = student),list)
    list = GetCompleteProject(Lecture.objects.filter(StudentNum = student),LectureRank.objects.filter(teacher = student),list)
    list = GetCompleteProject(Volunteering.objects.filter(StudentNum = student),VolunteeringRank.objects.filter(teacher = student),list)
    list = GetCompleteProject(SchoolActivity.objects.filter(StudentNum = student),SchoolActivityRank.objects.filter(teacher = student),list)
    list = GetCompleteSingle(StudentCadreRank.objects.filter(student = student),list)
    list = GetCompleteSingle(PaperRank.objects.filter(student = student),list)
    list = GetCompleteSingle(ExchangeRank.objects.filter(student = student),list)
    list = GetCompleteSingle(CompetitionRank.objects.filter(student = student),list)
    list = GetCompleteSingle(InternshipRank.objects.filter(student = student),list)
    return list

def clean(complete):
    complete.complete0 = 0
    complete.complete1 = 0
    complete.complete2 = 0
    complete.complete3 = 0
    complete.complete4 = 0
    complete.complete5 = 0
    complete.complete6 = 0
    complete.complete7 = 0
    complete.complete8 = 0
    complete.complete9 = 0
    return complete

def GetCompleteProject(links,ranks,list):
    if links:
      for link in links:
       if link.rankNum.Choice:
        list.complete0 += link.rankNum.Choice.complete.complete0
        list.complete1 += link.rankNum.Choice.complete.complete1
        list.complete2 += link.rankNum.Choice.complete.complete2
        list.complete3 += link.rankNum.Choice.complete.complete3
        list.complete4 += link.rankNum.Choice.complete.complete4
        list.complete5 += link.rankNum.Choice.complete.complete5
        list.complete6 += link.rankNum.Choice.complete.complete6
        list.complete7 += link.rankNum.Choice.complete.complete7
        list.complete8 += link.rankNum.Choice.complete.complete8
        list.complete9 += link.rankNum.Choice.complete.complete9
    if ranks:
     for project in ranks:
       if project.Choice:
        list.complete0 += project.Choice.complete.complete0
        list.complete1 += project.Choice.complete.complete1
        list.complete2 += project.Choice.complete.complete2
        list.complete3 += project.Choice.complete.complete3
        list.complete4 += project.Choice.complete.complete4
        list.complete5 += project.Choice.complete.complete5
        list.complete6 += project.Choice.complete.complete6
        list.complete7 += project.Choice.complete.complete7
        list.complete8 += project.Choice.complete.complete8
        list.complete9 += project.Choice.complete.complete9
    return list

def GetCompleteSingle(ranks,list):
    if ranks:
     for project in ranks:
       if project.Choice:
        list.complete0 += project.Choice.complete.complete0
        list.complete1 += project.Choice.complete.complete1
        list.complete2 += project.Choice.complete.complete2
        list.complete3 += project.Choice.complete.complete3
        list.complete4 += project.Choice.complete.complete4
        list.complete5 += project.Choice.complete.complete5
        list.complete6 += project.Choice.complete.complete6
        list.complete7 += project.Choice.complete.complete7
        list.complete8 += project.Choice.complete.complete8
        list.complete9 += project.Choice.complete.complete9
    return list

def GetCompleteTeam(links,list,student):
    if links:
     for link in links:
      if project.teacher == student:
       if link.rankNum.Choice:
        list.complete0 += link.rankNum.Choice.managerComplete.complete0
        list.complete1 += link.rankNum.Choice.managerComplete.complete1
        list.complete2 += link.rankNum.Choice.managerComplete.complete2
        list.complete3 += link.rankNum.Choice.managerComplete.complete3
        list.complete4 += link.rankNum.Choice.managerComplete.complete4
        list.complete5 += link.rankNum.Choice.managerComplete.complete5
        list.complete6 += link.rankNum.Choice.managerComplete.complete6
        list.complete7 += link.rankNum.Choice.managerComplete.complete7
        list.complete8 += link.rankNum.Choice.managerComplete.complete8
        list.complete9 += link.rankNum.Choice.managerComplete.complete9
      else:
       if link.rankNum.Choice:
        list.complete0 += link.rankNum.Choice.memberComplete.complete0
        list.complete1 += link.rankNum.Choice.memberComplete.complete1
        list.complete2 += link.rankNum.Choice.memberComplete.complete2
        list.complete3 += link.rankNum.Choice.memberComplete.complete3
        list.complete4 += link.rankNum.Choice.memberComplete.complete4
        list.complete5 += link.rankNum.Choice.memberComplete.complete5
        list.complete6 += link.rankNum.Choice.memberComplete.complete6
        list.complete7 += link.rankNum.Choice.memberComplete.complete7
        list.complete8 += link.rankNum.Choice.memberComplete.complete8
        list.complete9 += link.rankNum.Choice.memberComplete.complete9
    return list





