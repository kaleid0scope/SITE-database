from app.models import *
from django.contrib.auth.models import User

def GetComplete(request,student):
    complete = clean(student.complete)
    scores = Score.objects.filter(student = student)
    links = RankLinks.objects.filter(student = student)
    Clist = []
    for link in links:
        Clist.append(link.choice.complete)
    for s in scores:
        Clist.append(Mul(CompleteLM.objects.get(lesson = s.lesson , major = student.major),s.score))
    complete = Mix(Clist)
    complete.save()
    return complete

def clean(complete):
    complete = Complete()
    return complete

def Mul(complete,times):
        complete.complete0 == complete.complete0 * int(times)
        complete.complete1 == complete.complete1 * int(times)
        complete.complete2 == complete.complete2 * int(times)
        return complete

def Mix(list):
    complete = Complete()
    for comp in list:
        complete.complete0 += comp.complete0
        complete.complete1 += comp.complete1
        complete.complete2 += comp.complete2
    return complete
