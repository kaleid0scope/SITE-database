# -*- coding: utf-8 -*-

from app.models import *

def user_parameter(request):
    title = '综合测评系统'
    try:
        auth = Students.objects.get(user = request.user).auth
        if auth.isTeacher:
            type = '教师端'
        else:
            type = '学生端'
    except Exception,e:
        try:
            user = request.user
            if user.is_anonymous():
                type = '未登录'
            elif user.is_superuser:
                type = '管理员'
            else:
                type = '用户未认证'
        except Exception,e:
            type = '错误'
    return {'type':type,'title':title}