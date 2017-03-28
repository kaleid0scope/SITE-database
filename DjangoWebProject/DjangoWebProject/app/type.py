# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from app.models import PaperRank, Students



def GetType(request):
    error = []
    try:
        auth = Students.objects.get(user = request.user).auth
    except Exception,e:  
        error.append(e)
        return '未登录'
    if auth.isTeacher:
        return '教师端'
    return '学生端'

def render_with_type_(request,url,list):
    if 'title' not in list.keys():
        list['title'] = '学生综合测评系统'
    list['type'] = GetType(request)
    return render_to_response(url,list)

def render_with_type(link,request,url,list):
    if 'title' not in list.keys():
        list['title'] = '学生综合测评系统'
    list['type'] = GetType(request)
    list['name'] = link._meta.object_name
    return render_to_response(url,list)