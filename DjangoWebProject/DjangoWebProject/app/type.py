
from django.shortcuts import render_to_response
from app.models import PaperRank, Students, Inspectors



def GetType(request):
    error = []
    try:
        auth = Students.objects.get(user = request.user).auth
    except Exception,e:  
        error.append(e)
        return 0 #unlogin
    if request.user.is_superuser():
        return 3 #admin
    if auth.isTeacher:
        return 2 #teacher
    return 1     #student

def render_with_type(request,url,list):
    list['type'] = GetType(request)
    return render_to_response(url,list)