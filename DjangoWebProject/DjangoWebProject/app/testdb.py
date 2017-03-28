# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def createuser (username,email,password):
    user = User.objects.create_user(username = username, email = email , password = password)
    user.save()
    return HttpResponse("<p>creat user!</p>")

def setpassword (username,email,newpassword):
    u =User.objects.get(username = username)
    u.set_password(newpassword)
    u.save()