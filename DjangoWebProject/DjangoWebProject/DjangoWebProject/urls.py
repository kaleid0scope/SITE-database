# -*- coding: utf-8 -*-
"""
Definition of urls for DjangoWebProject.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
import DjangoWebProject.settings
import app.forms
import app.views
import app.testdb
from django.contrib import auth
from app.views import *
from app.project import *

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
from DjangoWebProject import settings
admin.autodiscover()

urlpatterns = [
    #url(r'/(?P<path>.*)','django.views.static.serve',{'document_root':settings.STATIC_ROOT+'/images'}), 
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
        },
        name='login'),
    url(r'^logout$',django.contrib.auth.views.logout,{'next_page': '/',},name='logout'),
    #url(r'^register$',app.views.register,),
    url(r'^search_form/$',search_form),
    url(r'^search/$',search),
    url(r'^reset',app.views.reset),
    url(r'^changepassword/(?P<username>\w+)/$',changepassword),  

    url(r'^complete/$',ShowComplete,name='complete'),
    url(r'^first/$',app.views.first),
    url(r'^copy/$',app.views.shit),

    url(r'^createlink/(?P<rankname>\w+)$',app.project.LinkCreate),
    url(r'^create/(?P<rankname>\w+)$',app.project.ProjectCreate),
    url(r'^Index/$',app.project.ProjectIndex),
    url(r'^Index/(?P<rankname>\w+)$',app.project.ProjectIndex),
    url(r'^check/(?P<linkid>\w+)$',app.project.ProjectCheck),
    url(r'^check/(?P<rankname>\w+)/(?P<linkid>\w+)$',app.project.ProjectCheck),
    url(r'^delete/(?P<linkid>\w+)$',app.project.ProjectDelete),
    url(r'^detail/(?P<linkid>\w+)$',app.project.ProjectDetail),


    url(r'^index/$',index,name='index'), 
    url(r'^construction/$',app.views.construction,name='construction'), 
    url(r'^excel/$',app.views.Excel),
    #C:\Users\Administrator\Source\Repos\SITE-database\DjangoWebProject\DjangoWebProject\app\static\images
    

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^i18n/', include('django.conf.urls.i18n')),
]
