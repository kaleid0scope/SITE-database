"""
Definition of urls for DjangoWebProject.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views
import DjangoWebProject.settings
import app.forms
import app.views
import app.exchange
import app.testdb
from app.views import search_form, search, changepassword,changeauth
from django.contrib import auth
from app.views import *
from app.ideology import *
from app.internship import *
from app.exchange import *
from app.lecture import *
from app.research import *
from app.schoolact import *
from app.volunteer import *
 

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
from DjangoWebProject import settings
admin.autodiscover()

urlpatterns = [
    #url(r'/(?P<path>.*)','django.views.static.serve',{'document_root':settings.STATIC_ROOT+'/images'}), 
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

    url(r'^first/$',app.views.first),

    url(r'^createResearch/$',app.research.createResearchProject),
    url(r'^research/(?P<id>\w+)/$',app.research.ResearchProject),
    url(r'^ResearchDetail/(?P<id>\w+)/$',app.research.ResearchProjectDetail), 
    url(r'^ResearchIndex/$',app.research.ResearchProjectIndex), 
    url(r'^JoinResearch/(?P<id>\w+)/$',app.research.JoinResearchProject), 
    url(r'^ResearchList/$',app.research.ResearchProjectList), 
    url(r'^ResearchSDetail/(?P<id>\w+)/$',app.research.ResearchProjectSDetail), 
    url(r'^CheckResearch/(?P<id>\w+)/(?P<isok>\w+)/$',app.research.CheckResearchProject), 

    url(r'^createPaper/$',createPaper),
    url(r'^paper/(?P<id>\w+)/$',app.views.paper),
    url(r'^PaperIndex/$',app.views.paperIndex),
    url(r'^createCompetition/$',createCompetition),
    url(r'^competition/(?P<id>\w+)/$',app.views.competition),
    url(r'^CompetitionIndex/$',app.views.competitionIndex),
    url(r'^createExchange/$',app.exchange.createExchange), 
    url(r'^exchange/(?P<id>\w+)/$',app.exchange.exchange),
    url(r'^ExchangeIndex/$',app.exchange.exchangeIndex),
    url(r'^createStudentCadre/$',createStudentCadre), 
    url(r'^studentCadre/(?P<id>\w+)/$',app.views.studentCadre),
    url(r'^StudentCadreIndex/$',app.views.studentCadreIndex),

    url(r'^createIdeologyConstruction/$',app.ideology.createIdeologyConstruction),
    url(r'^ideologyConstruction/(?P<id>\w+)/$',app.ideology.ideologyConstruction),
    url(r'^IdeologyConstructionDetail/(?P<id>\w+)/$',app.ideology.IdeologyConstructionDetail), 
    url(r'^IdeologyConstructionIndex/$',app.ideology.IdeologyConstructionIndex), 

    url(r'^JoinIdeologyConstruction/(?P<id>\w+)/$',app.ideology.JoinIdeologyConstruction),
    url(r'^IdeologyConstructionSDetail/(?P<id>\w+)/$',app.ideology.IdeologyConstructionSDetail), 
    url(r'^CheckIdeologyConstruction/(?P<id>\w+)/(?P<isok>\w+)/$',app.ideology.CheckIdeologyConstructions),  
    url(r'^IdeologyConstructionList/$',app.ideology.IdeologyConstructionList), 
    url(r'^createLecture/$',app.lecture.createLecture),
    url(r'^lecture/(?P<id>\w+)/$',app.lecture.lecture),
    url(r'^LectureDetail/(?P<id>\w+)/$',app.lecture.LectureDetail), 
    url(r'^LectureIndex/$',app.lecture.LectureIndex), 
    url(r'^JoinLecture/(?P<id>\w+)/$',app.lecture.JoinLecture), 

    url(r'^createVolunteering/$',app.volunteer.createVolunteering),
    url(r'^volunteering/(?P<id>\w+)/$',app.volunteer.volunteering),
    url(r'^VolunteeringDetail/(?P<id>\w+)/$',app.volunteer.VolunteeringDetail), 
    url(r'^VolunteeringIndex/$',app.volunteer.VolunteeringIndex),
    url(r'^VolunteeringList/$',app.volunteer.VolunteeringList), 
    url(r'^VolunteeringSDetail/(?P<id>\w+)/$',app.volunteer.VolunteeringSDetail), 
    url(r'^CheckVolunteering/(?P<id>\w+)/(?P<isok>\w+)/$',app.volunteer.CheckVolunteeringx),  
    url(r'^JoinVolunteering/(?P<id>\w+)/$',app.volunteer.JoinVolunteering), 

    url(r'^createSchoolActivity/$',app.schoolact.createSchoolActivity),
    url(r'^schoolActivity/(?P<id>\w+)/$',app.schoolact.schoolActivity),
    url(r'^SchoolActivityDetail/(?P<id>\w+)/$',app.schoolact.SchoolActivityDetail), 
    url(r'^SchoolActivityIndex/$',app.schoolact.SchoolActivityIndex),
    url(r'^CheckSchoolActivity/(?P<id>\w+)/(?P<isok>\w+)/$',app.schoolact.CheckSchoolActivityx),  
    url(r'^SchoolActivityList/$',app.schoolact.SchoolActivityList),  
    url(r'^SchoolActivitySDetail/(?P<id>\w+)/$',app.schoolact.SchoolActivitySDetail), 
    url(r'^JoinSchoolActivity/(?P<id>\w+)/$',app.schoolact.JoinSchoolActivity),  

    url(r'^createInternship/$',app.internship.createInternship), 
    url(r'^internship/(?P<id>\w+)/$',app.internship.internship),
    url(r'^InternshipDetail/(?P<id>\w+)/$',app.internship.InternshipDetail), 
    url(r'^InternshipIndex/$',app.internship.InternshipIndex), 
    url(r'^InternshipList/$',app.internship.InternshipList),  
    url(r'^CheckInternship/(?P<id>\w+)/(?P<isok>\w+)/$',app.internship.CheckInternship),  
    url(r'^InternshipSDetail/(?P<id>\w+)/$',app.internship.InternshipSDetail), 
    url(r'^JoinInternship/(?P<id>\w+)/$',app.internship.JoinInternship),  

    url(r'^index/$',index,name='index'), 
    url(r'^construction/$',app.views.construction,name='construction'), 
    url(r'^excel/$',Excel),
    
    #C:\Users\Administrator\Source\Repos\SITE-database\DjangoWebProject\DjangoWebProject\app\static\images
    

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^i18n/', include('django.conf.urls.i18n')),
]
