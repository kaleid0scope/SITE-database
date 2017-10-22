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
    return Error(request,e.message)#��ʵ��ʹ����Ӧʹ���û��ܽ��ܵ����Դ���e.messages,��"����ʧ�ܣ�blablablabla..."

@authenticated_required
def reply(request,messageid):
  try:
    message = Message.objects.get(id = messageid)
    if message.reciver != request.user: return Error(request,"����Ȩ�ظ�����Ϣ")
    if message.linkid and not result:  return Error(request,"��δ�Դ���Ϣ������Ч�ظ�")
    type = getType(request)
    if message.type == "����":
        if not type == "ѧ����": return Error(request,"������ѧ�����޷��ظ�����Ϣ")
        if result == 1:
            if not createMessage(request,message.sender,"���ã����Ѿ�ͬ������������blablabla","�ظ�"): return Error(request,"������Ϣʱʧ��")
            try:ranklink = RankLinks.objects.get(id = message.linkid)
            except Exception,e: return Error(request,"�Ҳ����������ᵽ����Ŀ")
            LinkAdd(request,rankname = ranklink.rname,rankid = ranklink.rtype,student = Students.objects.get(user = request.user))
        if result == 0:
            if not createMessage(request,message.sender,"���ã��Ҿܾ�����������blablabla","�ظ�"): return Error(request,"������Ϣʱʧ��")
    if message.type == "���":
        if not type == "����Ա" and not type == "����Ա" : return Error(request,"������ѧ�����޷��ظ�����Ϣ")
        return ProjectCheck(request,message.linkid)
    else :return Error(request,"���޷��Դ���Ϣ�����ظ�")
  except Exception,e:
    return Error(request,e.message)#��ʵ��ʹ����Ӧʹ���û��ܽ��ܵ����Դ���e.messages,��"�Ҳ�����Ҫ�ظ�����Ϣ"
    