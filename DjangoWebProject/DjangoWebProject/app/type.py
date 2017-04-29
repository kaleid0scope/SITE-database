# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from app.models import PaperRank, Students
from app.deco import *



def GetType(request):
    error = []
    try:
        auth = Students.objects.get(user = request.user).auth
    except Exception,e:
        return '未登录'
    if auth.isTeacher:
        return '教师端'
    return '学生端'

def render_with_type_(request,template_name,context):
    if 'title' not in context.keys():
        context['title'] = '学生综合测评系统'
    context['type'] = GetType(request)
    return render_to_response(template_name,context)

def render_with_type(link,request,template_name,context):
    if 'title' not in context.keys():
        context['title'] = '学生综合测评系统'
    context['type'] = GetType(request)
    context['name'] = link._meta.object_name
    return render_to_response(template_name,context)