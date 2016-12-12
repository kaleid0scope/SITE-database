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
    type = forms.ChoiceField(label='type', choices=(('teacher','teacher'),('student','student')))
 
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError('所有项都为必填项')
        elif self.cleaned_data['password2'] != self.cleaned_data['password']:
            raise forms.ValidationError('两次输入密码不一致')
        else:
            cleaned_data = super(RegisterForm, self).clean()
        return cleaned_data
 
