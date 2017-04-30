# -*- coding: utf-8 -*-

from django.http.response import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import Permission,User
from app.views import *
from app.type import *

def Ralert(*arg):
    def _deco(func):
        def __deco(template_name,context):
            if 'alert' not in context.keys():
                context['alert'] = arg
            return func(template_name,context)
        return __deco  
    return _deco

def teacher_required(func):
    def _deco(request):
        if request.user.has_perm('auth.is_instructor'):
            Response = func(request)
        else:
            Response = Ralert('teacher_required')(render_to_response)('app/index.html',{'title':'学生综合测评系统',})
        return Response
    return _deco
    