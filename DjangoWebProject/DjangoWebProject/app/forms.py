# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from cProfile import label

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

class CreateResearchProjectForm(forms.Form):
    ProjectName = forms.CharField(required=True,
        label=u"科研立项名称",
        error_messages={'required': u'请输入科研立项名称'})
    ProjectTime = forms.DateField(required=True,
        label=u"项目时间",
        error_messages={'required': u'请输入项目时间'})

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"错误")
        else:
            cleaned_data = super(CreateResearchProjectForm, self).clean()
        return cleaned_data

class CreatePaperForm(forms.Form):#期刊名称? 支撑文件 是否需要审核 对应两个类?
    ProjectName = forms.CharField(required=True,
        label=u"论文题目",
        error_messages={'required': u'请输入论文题目'})
    ProjectTime = forms.DateField(required=True,
        label=u"发表时间",
        error_messages={'required': u'请输入论文发表时间'})
    
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"错误")
        else:
            cleaned_data = super(CreatePaperForm, self).clean()
        return cleaned_data
    '''   SupportText = forms.FileField(upload_to = './upload/')'''

class CreateCompetitionForm(forms.Form):
    ProjectName = forms.CharField(required=True,
        label=u"竞赛名称",
        error_messages={'required': u'请输入竞赛名称'})
    ProjectTime = forms.DateField(required=True,
        label=u"竞赛时间",
        error_messages={'required': u'请输入竞赛时间'})

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"错误")
        else:
            cleaned_data = super(CreateCompetitionForm, self).clean()
        return cleaned_data

class CreateExchangeForm(forms.Form):
    ProjectName = forms.CharField(required=True,
        label=u"交流交换项目名称",
        error_messages={'required': u'请输入交流交换项目名称'})
    startTime = forms.DateField(required=True,
        label=u"派出时间",
        error_messages={'required': u'请输入派出时间'})
    endTime = forms.DateField(required=True,
        label=u"返校时间",
        error_messages={'required': u'请输入竞赛时间'})
    ProjectContent = forms.Textarea(required=True,
        label=u"交流内容",
        error_messages={'required': u'请输入交流内容'})
    SupportText = forms.Textarea(required=True,
        label=u"支撑文档",
        error_messages={'required': u'请输入支撑文档'})
    type = forms.CharField(required=True,
        label=u"交流类型",
        error_messages={'required': u'请输入交流交换项目名称'})
    nature = forms.CharField(required=True,
        label=u"交流性质",
        error_messages={'required': u'请输入交流性质'})

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"错误")
        else:
            cleaned_data = super(CreateExchangeForm, self).clean()
        return cleaned_data

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

class ChangeauthForm(forms.Form):
    isTeacher = forms.BooleanField(required=False,
        label=u"是否为教师")
    research = forms.BooleanField(required=False,
        label=u"科研立项")
    paper = forms.BooleanField(required=False,
        label=u"论文")
    competition = forms.BooleanField(required=False,
        label=u"竞赛")
    exchange = forms.BooleanField(required=False,
        label=u"交流交换")
    ideologyConstruction = forms.BooleanField(required=False,
        label=u"思想活动")
    lecture = forms.BooleanField(required=False,
        label=u"讲座活动")
    volunteering = forms.BooleanField(required=False,
        label=u"志愿活动")
    schoolActivity = forms.BooleanField(required=False,
        label=u"校园活动")
    internship = forms.BooleanField(required=False,
        label=u"实践活动")
    studentCadre = forms.BooleanField(required=False,
        label=u"学生干部")

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"错误")
        else:
            cleaned_data = super(ChangeauthForm, self).clean()
        return cleaned_data