# -*- coding: utf-8 -*-

from app.models import *

def user_parameter(request):
    title = '综合测评系统'
    if request.user.is_authenticated():
        if request.user.is_superuser:
            type = '管理员'
        elif request.user.has_perm('auth.is_instructor'):
            type = '教师端'
        else:
            try:
                student = Students.objects.get()
                type = '学生端'
            except Exception,e:
                type = '学生未认证'
    else:
        type = '未登录'
    return {'type':type,'title':title}