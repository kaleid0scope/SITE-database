#coding:utf-8
"""Definition of forms.
"""

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
                                   'placeholder':'password'}))

#注册表单
class RegisterForm(forms.Form):
    username = forms.CharField(label=_("username"),max_length=100,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
    password2 = forms.CharField(label=_("Password"),widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'ConfirmPassword'}))
    email = forms.EmailField(widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'email'}))
    #type = forms.ChoiceField(label='type', choices=(('teacher','laoshi'),('student','xuesheng')))
 
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError('所有项都为必填项')
        elif self.cleaned_data['password2'] != self.cleaned_data['password']:
            raise forms.ValidationError('两次输入密码不一致')
        else:
            cleaned_data = super(RegisterForm, self).clean()
        return cleaned_data
 
#登陆表单
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',widget=forms.TextInput(attrs={"placeholder": "用户名", "required": "required",}),
                               max_length=50, error_messages={"required": "username不能为空",})
    password = forms.CharField(label='密码',widget=forms.PasswordInput(attrs={"placeholder": "密码", "required": "required",}),
                               max_length=20, error_messages={"required": "password不能为空",})

class UserForm(forms.Form): 
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
