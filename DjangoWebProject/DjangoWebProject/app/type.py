# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from app.models import PaperRank, Students
from app.deco import *



def GetType(request):
    error = []
    if request.user.has_perm('auth.is_instructor'):
        return '教师端'
    else:
        return '学生端'
    return '未登录'

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