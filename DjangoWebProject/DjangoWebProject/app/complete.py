from app.models import *
from django.contrib.auth.models import User

def GetComplete(request,student):
    complete = clean(student.complete)
    scores = Score.objects.filter(student = student)
    links = RankLinks.objects.filter(student = student)
    Clist = []
    for link in links:
        if link.choice : Clist.append(link.choice.complete)
    for s in scores:
        Clist.append(Mul( CompleteLM.objects.get(lesson = s.lesson , major = student.major).complete , s.score))
    complete = Mix(Clist)
    complete.save()
    return complete

def clean(complete):
    complete = Complete()
    return complete

def Mul(complete,times,comp = None):
        complete.complete0 = complete.complete0 * int(times)
        complete.complete1 = complete.complete1 * int(times)
        complete.complete2 = complete.complete2 * int(times)
        complete.complete3 = complete.complete3 * int(times)
        complete.complete4 = complete.complete4 * int(times)
        complete.complete5 = complete.complete5 * int(times)
        complete.complete6 = complete.complete6 * int(times)
        complete.complete7 = complete.complete7 * int(times)
        complete.complete8 = complete.complete8 * int(times)
        complete.complete9 = complete.complete9 * int(times)
        complete.complete10 = complete.complete10 * int(times)
        complete.complete11 = complete.complete11 * int(times)
        complete.complete12 = complete.complete12 * int(times)
        complete.complete13 = complete.complete13 * int(times)
        complete.complete14 = complete.complete14 * int(times)
        complete.complete15 = complete.complete15 * int(times)
        complete.complete16 = complete.complete16 * int(times)
        complete.complete17 = complete.complete17 * int(times)
        complete.complete18 = complete.complete18 * int(times)
        complete.complete19 = complete.complete19 * int(times)
        complete.complete20 = complete.complete20 * int(times)
        complete.complete21 = complete.complete21 * int(times)
        complete.complete22 = complete.complete22 * int(times)
        complete.complete23 = complete.complete23 * int(times)
        complete.complete24 = complete.complete24 * int(times)
        complete.complete25 = complete.complete25 * int(times)
        complete.complete26 = complete.complete26 * int(times)
        complete.complete27 = complete.complete27 * int(times)
        complete.complete28 = complete.complete28 * int(times)
        complete.complete29 = complete.complete29 * int(times)
        if comp:
            complete.complete0 *= comp.complete0
            complete.complete1 *= comp.complete1
            complete.complete2 *= comp.complete2
            complete.complete3 *= comp.complete3
            complete.complete4 *= comp.complete4
            complete.complete5 *= comp.complete5
            complete.complete6 *= comp.complete6
            complete.complete7 *= comp.complete7
            complete.complete8 *= comp.complete8
            complete.complete9 *= comp.complete9
            complete.complete10 *= comp.complete10
            complete.complete11 *= comp.complete11
            complete.complete12 *= comp.complete12
            complete.complete13 *= comp.complete13
            complete.complete14 *= comp.complete14
            complete.complete15 *= comp.complete15
            complete.complete16 *= comp.complete16
            complete.complete17 *= comp.complete17
            complete.complete18 *= comp.complete18
            complete.complete19 *= comp.complete19
            complete.complete20 *= comp.complete20
            complete.complete21 *= comp.complete21
            complete.complete22 *= comp.complete22
            complete.complete23 *= comp.complete23
            complete.complete24 *= comp.complete24
            complete.complete25 *= comp.complete25
            complete.complete26 *= comp.complete26
            complete.complete27 *= comp.complete27
            complete.complete28 *= comp.complete28
            complete.complete29 *= comp.complete29
        return complete

def Mix(list):
    complete = Complete()
    for comp in list:
        complete.complete0 += comp.complete0
        complete.complete1 += comp.complete1
        complete.complete2 += comp.complete2
        complete.complete3 += comp.complete3
        complete.complete4 += comp.complete4
        complete.complete5 += comp.complete5
        complete.complete6 += comp.complete6
        complete.complete7 += comp.complete7
        complete.complete8 += comp.complete8
        complete.complete9 += comp.complete9
        complete.complete10 += comp.complete10
        complete.complete11 += comp.complete11
        complete.complete12 += comp.complete12
        complete.complete13 += comp.complete13
        complete.complete14 += comp.complete14
        complete.complete15 += comp.complete15
        complete.complete16 += comp.complete16
        complete.complete17 += comp.complete17
        complete.complete18 += comp.complete18
        complete.complete19 += comp.complete19
        complete.complete20 += comp.complete20
        complete.complete21 += comp.complete21
        complete.complete22 += comp.complete22
        complete.complete23 += comp.complete23
        complete.complete24 += comp.complete24
        complete.complete25 += comp.complete25
        complete.complete26 += comp.complete26
        complete.complete27 += comp.complete27
        complete.complete28 += comp.complete28
        complete.complete29 += comp.complete29
    return complete
