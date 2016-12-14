# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class ResetPasswordForm(forms.Form):
    username = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class RegisterForm(forms.Form):  
    username = forms.CharField()  
    email = forms.EmailField()  
    password = forms.CharField(widget=forms.PasswordInput)  
    password2= forms.CharField(label='Confirm',widget=forms.PasswordInput)  
    def pwd_validate(self,p1,p2):  
        return p1==p2  

class ChangepwdForm(forms.Form):
    old_pwd = forms.CharField(required=True,
        label=u"原密码",
        error_messages={'required': u'请输入原密码'},
        widget=forms.PasswordInput(attrs={
                'placeholder':u"原密码",
            }),) 
    new_pwd = forms.CharField(required=True,
        label=u"新密码",
        error_messages={'required': u'请输入新密码'},
        widget=forms.PasswordInput(attrs={
                'placeholder':u"新密码",
            }),)
    new_pwd2 = forms.CharField(required=True,
        label=u"确认密码",
        error_messages={'required': u'请再次输入新密码'},
        widget=forms.PasswordInput(attrs={
                'placeholder':u"确认密码",
            }),)

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        elif self.cleaned_data['new_pwd'] <> self.cleaned_data['new_pwd2']:
            raise forms.ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(ChangepwdForm, self).clean()
        return cleaned_data


class ChangepwdForm(forms.Form):
    isTeacher = forms.BooleanField(required=True,
        label=u"是否为教师",
        error_messages={'required': u'请确认是否所有值已经输入'})
    research = forms.BooleanField(required=True,
        label=u"科研立项",
        error_messages={'required': u'请确认是否所有值已经输入'})
    paper = forms.BooleanField(required=True,
        label=u"论文",
        error_messages={'required': u'请确认是否所有值已经输入'})
    competition = forms.BooleanField(required=True,
        label=u"竞赛",
        error_messages={'required': u'请确认是否所有值已经输入'})
    exchange = forms.BooleanField(required=True,
        label=u"交流交换",
        error_messages={'required': u'请确认是否所有值已经输入'})
    ideologyConstruction = forms.BooleanField(required=True,
        label=u"思想活动",
        error_messages={'required': u'请确认是否所有值已经输入'})
    lecture = forms.BooleanField(required=True,
        label=u"讲座活动",
        error_messages={'required': u'请确认是否所有值已经输入'})
    volunteering = forms.BooleanField(required=True,
        label=u"志愿活动",
        error_messages={'required': u'请确认是否所有值已经输入'})
    schoolActivity = forms.BooleanField(required=True,
        label=u"校园活动",
        error_messages={'required': u'请确认是否所有值已经输入'})
    internship = forms.BooleanField(required=True,
        label=u"实践活动",
        error_messages={'required': u'请确认是否所有值已经输入'})
    studentCadre = forms.BooleanField(required=True,
        label=u"学生干部",
        error_messages={'required': u'请确认是否所有值已经输入'})

class CreateResearchProjectForm(forms.Form):
    ProjectName = forms.CharField(required=True,
        label=u"科研立项名称",
        error_messages={'required': u'请输入科研立项名称'})
    teacherNum = forms.IntegerField(required=True,
        label=u"创建者学号",
        error_messages={'required': u'请输入创建者学号'})
    ProjectTime = forms.DateField(required=True,
        label=u"项目时间",
        error_messages={'required': u'请输入项目时间'})
"""    rank = forms.CharField(required=True,
        label=u"科研立项等级",
        error_messages={'required': u'请输入科研立项等级'})
    score = forms.IntegerField(required=True,
        label=u"科研立项分级评分",
        error_messages={'required': u'请输入科研立项分级评分'})
    role = forms.CharField(required=True,
        label=u"科研立项角色",
        error_messages={'required': u'请输入“负责人”或“成员”'})
    startingTime = forms.DateField(required=True,
        label=u"分级评分起始有效时间",
        error_messages={'required': u'请输入分级评分起始有效时间'})"""

class JoinResearchProjectForm(forms.Form):
    StudentNum = forms.IntegerField(required=True,
        label=u"学号",
        error_messages={'required': u'请输入学号'})
    rankNum = forms.IntegerField(required=True,
        label=u"科研立项分级编号",
        error_messages={'required': u'请输入科研立项分级编号'})
    ProjectName = forms.CharField(required=True,
        label=u"项目名称",
        error_messages={'required': u'请输入项目名称'})
    ProjectTime = forms.DateField(required=True,
        label=u"项目时间",
        error_messages={'required': u'请输入项目时间'})