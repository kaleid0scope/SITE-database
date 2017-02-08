
from django.shortcuts import render_to_response
from app.models import PaperRank, Students, Inspectors



def GetType(request):
    error = []
    try:
        auth = Students.objects.get(user = request.user).auth
    except Exception,e:  
        error.append(e)
        return 0 #未登录
    if auth.isTeacher:
        return 2 #是教师
    return 1     #是学生