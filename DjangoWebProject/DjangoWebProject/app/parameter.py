# -*- coding: utf-8 -*-

from app.models import *

def user_parameter(request):
    title = 'SITE综合测评系统'
    if request.user.is_authenticated():
        if request.user.is_superuser:
            type = '管理员'
        elif request.user.has_perm('auth.is_instructor'):
            type = '辅导员'
        else:
            try:
                teacher = Teacher.objects.get(user = request.user)
                type = '教师端'
            except Exception,e:
                try:
                    student = Students.objects.get(user = request.user)
                    type = '学生端'
                except Exception,e:
                    type = '学生未认证'
    else:
        type = '未登录'
    return {'type':type,'title':title}