# -*- coding: utf-8 -*-

from django.http.response import HttpResponse
from django.shortcuts import render_to_response
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
        if False:
            Response = func(request)
        else:
            Response = Ralert('teacher_required')(render_to_response)('app/index.html',{'title':'学生综合测评系统',})
        return Response
    return _deco
    