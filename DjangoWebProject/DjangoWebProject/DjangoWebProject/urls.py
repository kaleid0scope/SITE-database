# -*- coding: utf-8 -*-
"""
Definition of urls for DjangoWebProject.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
import DjangoWebProject.settings
from django.contrib import auth
import app
from app.views import *
from app.project import *
from app.project import *

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
from DjangoWebProject import settings
admin.autodiscover()

urlpatterns = [
    #url(r'/(?P<path>.*)','django.views.static.serve',{'document_root':settings.STATIC_ROOT+'/images'}), 
    url(r'^$', home, name='home'),
    url(r'^contact$', contact, name='contact'),
    url(r'^about', about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
        },
        name='login'),
    url(r'^logout$',django.contrib.auth.views.logout,{'next_page': '/',},name='logout'),
    #url(r'^register$',register,),
    url(r'^search_form/$',search_form),
    url(r'^search/$',search),
    url(r'^reset',reset),
    url(r'^changepassword/(?P<username>\w+)/$',changepassword),  

    url(r'^test',test),

    url(r'^complete/$',ShowComplete,name='complete'),
    url(r'^complete/(?P<id>\w+)$',ShowComplete,name='complete'),
    url(r'^studentIndex/(?P<studentid>\w+)$',ProjectIndex),
    url(r'^first/$',first),
    url(r'^copy/$',shit),

    url(r'^add/(?P<rankname>\w+)/(?P<rankid>\w+)$',LinkAdd),
    url(r'^add/(?P<rankname>\w+)/(?P<rankid>\w+)/(?P<student>\w+)$',LinkAdd),
    url(r'^create/(?P<rankname>\w+)$',ProjectCreate,name = 'create'),
    url(r'^Index/$',ProjectIndex,name = 'project'),
    url(r'^Index/(?P<rankname>\w+)$',ProjectIndex),
    url(r'^check/(?P<linkid>\w+)$',ProjectCheck),
    url(r'^check/(?P<rankname>\w+)/(?P<linkid>\w+)$',ProjectCheck),
    url(r'^Check/(?P<linkid>\w+)$',ProjectCheck),
    url(r'^Check/(?P<rankname>\w+)/(?P<linkid>\w+)$',ProjectCheck),
    url(r'^delete/(?P<linkid>\w+)$',ProjectDelete),
    url(r'^detail/(?P<linkid>\w+)$',ProjectDetail),
    url(r'^Detail/(?P<linkid>\w+)$',ProjectDetail),
    url(r'^Add/(?P<linkid>\w+)/(?P<sid>\w+)$',ProjectAdd),

    url(r'^construction/$',construction,name='construction'), 
    url(r'^excel/$',Excel),
    #C:\Users\Administrator\Source\Repos\SITE-database\DjangoWebProject\DjangoWebProject\app\static\images
    

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^i18n/', include('django.conf.urls.i18n')),
]
