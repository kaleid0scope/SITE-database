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
from app.views import createResearchProject ,createPaper,createCompetition,createExchange,createIdeologyConstruction ,createLecture,createVolunteering ,createSchoolActivity,createInternship ,createStudentCadre
from app.views import researchProject,index,Excel,ResearchProjectIndex,IdeologyConstructionIndex,LectureIndex,VolunteeringIndex,SchoolActivityIndex,InternshipIndex,ResearchProjectDetail
from app.views import ResearchProjectDetail
from app.views import JoinResearchProject

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
    url(r'^researchProject/(?P<id>\w+)/$',researchProject),
    url(r'^ResearchProjectDetail/(?P<id>\w+)/$',ResearchProjectDetail), 
    url(r'^ResearchProjectIndex/$',ResearchProjectIndex), 
    url(r'^JoinResearchProject/(?P<id>\w+)/$',JoinResearchProject), 

    url(r'^createPaper/$',createPaper),
    url(r'^createCompetition/$',createCompetition),
    url(r'^createExchange/$',createExchange), 
    url(r'^createStudentCadre/$',createStudentCadre), 

    url(r'^createIdeologyConstruction/$',createIdeologyConstruction),
    url(r'^IdeologyConstructionIndex/$',IdeologyConstructionIndex), 

    url(r'^createLecture/$',createLecture),
    url(r'^IdeologyConstructionIndex/$',LectureIndex), 

    url(r'^createVolunteering/$',createVolunteering),
    url(r'^IdeologyConstructionIndex/$',VolunteeringIndex), 

    url(r'^createSchoolActivity/$',createSchoolActivity),
    url(r'^IdeologyConstructionIndex/$',SchoolActivityIndex), 

    url(r'^createInternship/$',createInternship), 
    url(r'^IdeologyConstructionIndex/$',InternshipIndex), 
    url(r'^index/$',index), 
    url(r'^excel/$',Excel),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^i18n/', include('django.conf.urls.i18n')),
]
