from app.models import *
from django.contrib.auth.models import User

def GetComplete(request,student):
    list = []
    GetCompleteTeam(ResearchProject.objects.filter(StudentNum = student),list)
    GetCompleteProject(IdeologyConstruction.objects.filter(StudentNum = student),list)
    GetCompleteProject(Lecture.objects.filter(StudentNum = student),list)
    GetCompleteProject(Volunteering.objects.filter(StudentNum = student),list)
    GetCompleteProject(Internship.objects.filter(StudentNum = student),list)
    GetCompleteProject(SchoolActivity.objects.filter(StudentNum = student),list)
    GetCompleteSingle(StudentCadreRank.objects.filter(StudentNum = student),list)
    GetCompleteSingle(PaperRank.objects.filter(StudentNum = student),list)
    GetCompleteSingle(ExchangeRank.objects.filter(StudentNum = student),list)
    GetCompleteSingle(CompetitionRank.objects.filter(StudentNum = student),list)
    complete = student.complete
    complete.complete1 == list[1]
    complete.complete2 == list[2]
    complete.complete3 == list[3]
    complete.complete4 == list[4]
    complete.complete5 == list[5]
    complete.complete6 == list[6]
    complete.complete7 == list[7]
    complete.complete8 == list[8]
    complete.complete9 == list[9]
    complete.complete0 == list[0]
    complete.save()
    return list

def GetCompleteProject(links,list):
    for link in links:
        list[0] += link.rankNum.Choices.complete.complete0
        list[1] += link.rankNum.Choices.complete.complete1
        list[2] += link.rankNum.Choices.complete.complete2
        list[3] += link.rankNum.Choices.complete.complete3
        list[4] += link.rankNum.Choices.complete.complete4
        list[5] += link.rankNum.Choices.complete.complete5
        list[6] += link.rankNum.Choices.complete.complete6
        list[7] += link.rankNum.Choices.complete.complete7
        list[8] += link.rankNum.Choices.complete.complete8
        list[9] += link.rankNum.Choices.complete.complete9

def GetCompleteSingle(ranks,list):
    for project in ranks:
        list[0] += project.Choices.complete.complete0
        list[1] += project.Choices.complete.complete1
        list[2] += project.Choices.complete.complete2
        list[3] += project.Choices.complete.complete3
        list[4] += project.Choices.complete.complete4
        list[5] += project.Choices.complete.complete5
        list[6] += project.Choices.complete.complete6
        list[7] += project.Choices.complete.complete7
        list[8] += project.Choices.complete.complete8
        list[9] += project.Choices.complete.complete9

def GetCompleteTeam(links,list,student):
    for link in links:
      if project.teacher == student:
        list[0] += link.rankNum.Choices.managerComplete.complete0
        list[1] += link.rankNum.Choices.managerComplete.complete1
        list[2] += link.rankNum.Choices.managerComplete.complete2
        list[3] += link.rankNum.Choices.managerComplete.complete3
        list[4] += link.rankNum.Choices.managerComplete.complete4
        list[5] += link.rankNum.Choices.managerComplete.complete5
        list[6] += link.rankNum.Choices.managerComplete.complete6
        list[7] += link.rankNum.Choices.managerComplete.complete7
        list[8] += link.rankNum.Choices.managerComplete.complete8
        list[9] += link.rankNum.Choices.managerComplete.complete9
      else:
        list[0] += link.rankNum.Choices.memberComplete.complete0
        list[1] += link.rankNum.Choices.memberComplete.complete1
        list[2] += link.rankNum.Choices.memberComplete.complete2
        list[3] += link.rankNum.Choices.memberComplete.complete3
        list[4] += link.rankNum.Choices.memberComplete.complete4
        list[5] += link.rankNum.Choices.memberComplete.complete5
        list[6] += link.rankNum.Choices.memberComplete.complete6
        list[7] += link.rankNum.Choices.memberComplete.complete7
        list[8] += link.rankNum.Choices.memberComplete.complete8
        list[9] += link.rankNum.Choices.memberComplete.complete9





