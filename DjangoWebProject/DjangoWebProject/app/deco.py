# -*- coding: utf-8 -*-

from django.http.response import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import Permission,User
from app.models import *

def Ralert(*arg):
    def _deco(func):
        def __deco(request,template_name,context,**kargs):
            if 'alert' not in context.keys():
                context['alert'] = arg
            else:
                context['alert'].extend(arg)
            return func(request,template_name,context,**kargs)
        return __deco  
    return _deco

def teacher_required(func):
    def _deco(request,**kargs):
        if request.user.has_perm('auth.is_instructor'):
            Response = func(request,**kargs)
        else:
            assert isinstance(request, HttpRequest)
            Response = Ralert('teacher_required')(render)(request,'app/index.html',{})
        return Response
    return _deco

def authenticated_required(func):
    def _deco(request,**kargs):
        if Students.objects.filter(user = request.user) or request.user.has_perm('auth.is_instructor'):
            Response = func(request,**kargs)
        else:
            assert isinstance(request, HttpRequest)
            Response = Ralert('student_required')(render)(request,'app/index.html',{})
        return Response
    return _deco