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

@authenticated_required
def createMessage(request,toUser,text,type = None,linkid = None):
  try:
    message = Message(text = text,sender = request.user,reciver = toUser,type = type , linkid = linkid , time = datetime.now)
    message.save()
    return True
  except Exception,e:
    return Error(request,e.message)#在实际使用中应使用用户能接受的语言代替e.messages,如"创建失败，blablablabla..."

@authenticated_required
def reply(request,messageid):
  try:
    message = Message.objects.get(id = messageid)
    if message.reciver != request.user: return Error(request,"您无权回复此消息")
    if message.linkid and not result:  return Error(request,"您未对此消息做出有效回复")
    type = getType(request)
    if message.type == "邀请":
        if not type == "学生端": return Error(request,"您并非学生，无法回复此消息")
        if result == 1:
            if not createMessage(request,message.sender,"您好，我已经同意了您的邀请blablabla","回复"): return Error(request,"创建信息时失败")
            try:ranklink = RankLinks.objects.get(id = message.linkid)
            except Exception,e: return Error(request,"找不到邀请中提到的项目")
            LinkAdd(request,rankname = ranklink.rname,rankid = ranklink.rtype,student = Students.objects.get(user = request.user))
        if result == 0:
            if not createMessage(request,message.sender,"您好，我拒绝了您的邀请blablabla","回复"): return Error(request,"创建信息时失败")
    if message.type == "审核":
        if not type == "辅导员" and not type == "管理员" : return Error(request,"您并非学生，无法回复此消息")
        return ProjectCheck(request,message.linkid)
    else :return Error(request,"您无法对此消息做出回复")
  except Exception,e:
    return Error(request,e.message)#在实际使用中应使用用户能接受的语言代替e.messages,如"找不到您要回复的消息"
    