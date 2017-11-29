# -*- coding: utf-8 -*-
from app.forms import *
from app.models import *
from app.parameter import *
from app.Info import *
from app.deco import *
from app.project import *
from django.shortcuts import *
from django.contrib.auth.models import User
from DjangoWebProject import settings
from django.http import HttpRequest
from django.template import RequestContext
from app.create import *
from django.template.loader import get_template
from django.contrib.auth.decorators import * 
from __builtin__ import *
from app.views import *

def authTest(request):
    if getType(request) !=  '学生端' and getType(request) !=  '教师端' and getType(request) !=  '辅导员' and getType(request) !=  '管理员' : return Error(request,"请先登录")


def createMessage(request,toUser,text,type = None,linkid = None):
  try:
    authTest(request)
    message = Message(text = text,sender = request.user,reciver = toUser,type = type , linkid = linkid , Time = datetime.now())
    message.save()
    return True
  except Exception,e:
    #实际使用中e.messages用特定提示替代（创建失败）之类"
    return Error(request,e.message)

@authenticated_required
def markMessage(request):
  try:
    messages = Message.objects.filter(reciver = request.user).filter(isRead = 0)
    for message in messages:
        message.isRead = 1
        message.save()
    return redirect(request.META['HTTP_REFERER'])
  except Exception,e:
    #实际使用中e.messages用特定提示替代"
    return Error(request,e.message)

def readMessage(request,messageid = None):
    if messageid: 
        message = Message.objects.get(id = messageid)
        message.isRead = 1
        message.save()
    return redirect(request.META['HTTP_REFERER'])

def replyMessage(request,messageid,result):
 # try:
    authTest(request)
    message = Message.objects.get(id = messageid)
    if message.reciver != request.user: return Error(request,"您无权回复此消息")
    if not result:  return Error(request,"您尚未作出回复")
    message.isRead = 1
    message.save()
    if message.type == "邀请":
        #if not type == "学生端": return Error(request,"您无法回复此消息")
        if result == 1 or result == u'1':
            try:ranklink = RankLinks.objects.get(id = message.linkid)
            except Exception,e: return Error(request,"找不到邀请中的项目，回复失败")
            if not createMessage(request,message.sender,"我已经同意了您的请求blablabla","回复"): return Error(request,"回复失败")
            LinkAdd(request,rankname = ranklink.rtype,rankid = ranklink.rnum,student = Students.objects.get(user = request.user))
            return redirect(request.META['HTTP_REFERER'])
        if result == 0 or result == u'0':
            if not createMessage(request,message.sender,"我拒绝了您的请求blablabla","回复"): return Error(request,"回复失败")
            return redirect(request.META['HTTP_REFERER'])
    if message.type == "审核":
        if not type == "管理员" and not type == "辅导员" : return Error(request,"您无权回复此消息")
        return ProjectCheck(request,message.linkid)
    else :return Error(request,"该消息无法回复")
'''except Exception,e:
    #实际使用中e.messages用特定提示替代"
    return Error(request,e.message)'''
    