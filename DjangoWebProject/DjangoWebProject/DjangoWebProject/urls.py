"""
Definition of urls for DjangoWebProject.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views
import app.testdb
from app.views import search_form, search, changepassword,changeauth
from django.contrib import auth
from app.views import search_form, search, changepassword
from app.views import createResearchProject ,createPaper
from app.views import createCompetition,createExchange,createIdeologyConstruction ,createLecture,createVolunteering ,createSchoolActivity,createInternship ,createStudentCadre,ResearchProject,index

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about', app.views.about, name='about'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Log in',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^testdb', app.testdb.testdb),
    #url(r'^register$',app.views.register,),
    url(r'^search_form/$',search_form),
    url(r'^search/$',search),
    url(r'^reset',app.views.reset),
    url(r'^changepassword/(?P<username>\w+)/$',changepassword),  
    url(r'^changeauth/(?P<username>\w+)/$',changeauth),    
    url(r'^createResearchProject/$',createResearchProject),  
    url(r'^ResearchProject/(?P<id>\w+)/$',ResearchProject),
    url(r'^createPaper/$',createPaper),  
    url(r'^createCompetition/$',createCompetition),  
    url(r'^createExchange/$',createExchange),  
    url(r'^createIdeologyConstruction/$',createIdeologyConstruction),  
    url(r'^createLecture/$',createLecture),  
    url(r'^createVolunteering/$',createVolunteering),  
    url(r'^createSchoolActivity/$',createSchoolActivity),  
    url(r'^createInternship/$',createInternship),  
    url(r'^createStudentCadre/$',createStudentCadre), 
    url(r'^index/$',index), 

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^i18n/', include('django.conf.urls.i18n')),
]
