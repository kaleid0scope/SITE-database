from app.type import *
from app.models import *

def getInfo(request,model):
    try:
        student = Students.objects.get(user = request.user)
        selfProjects = model.objects.filter(teacher = student)
    except Exception,e:
        error = e
        return render_with_type_(request,error.html,{'alert':error})
    return {'student':student,'projects':selfProjects}

def getInfo(request):
    try:
        student = Students.objects.get(user = request.user)
    except Exception,e:
        error = e
        return render_with_type_(request,error.html,{'alert':error})
    return {'student':student}

def getInfo(request,model,id):
    try:
        student = Students.objects.get(user = request.user)
        selfProjects = model.objects.filter(teacher = student)
        thisProject = model.objects.get(id = int(id))
    except Exception,e:
        error = e
        return render_with_type_(request,error.html,{'alert':error})
    return {'student':student,'projects':selfProjects,'target':thisProject}