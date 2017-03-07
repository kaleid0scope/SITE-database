from app.type import *
from app.models import *

def getInfo(request,model):
    try:
        student = Students.objects.get(user = request.user)
        insp = Inspectors.objects.get(number = 10002)
        selfProjects = model.objects.filter(teacher = student)
    except Exception,e:
        error = e
        return render_with_type(request,error.html,{'alert':error})
    return {'student':student,'insp':insp,'projects':selfProjects}

def getInfo(request):
    try:
        student = Students.objects.get(user = request.user)
        insp = Inspectors.objects.get(number = 10002)
    except Exception,e:
        error = e
        return render_with_type(request,error.html,{'alert':error})
    return {'student':student,'insp':insp}

def getInfo(request,model,id):
    try:
        student = Students.objects.get(user = request.user)
        insp = Inspectors.objects.get(number = 10002)
        selfProjects = model.objects.filter(teacher = student)
        thisProject = model.objects.get(id = int(id))
    except Exception,e:
        error = e
        return render_with_type(request,error.html,{'alert':error})
    return {'student':student,'insp':insp,'projects':selfProjects,'target':thisProject}