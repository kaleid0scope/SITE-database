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

    url(r'^first/$',app.views.first),
    url(r'^copy/$',app.views.shit),

    url(r'^createResearch/$',createResearchProject),
    url(r'^research/(?P<id>\w+)/$',researchProject),
    url(r'^ResearchDetail/(?P<id>\w+)/$',ResearchProjectDetail), 
    url(r'^ResearchIndex/$',ResearchProjectIndex), 
    url(r'^JoinResearch/(?P<id>\w+)/$',JoinResearchProject), 
    url(r'^ResearchList/$',ResearchProjectList), 
    url(r'^ResearchSDetail/(?P<id>\w+)/$',ResearchProjectSDetail), 
    url(r'^CheckResearch/(?P<id>\w+)/(?P<isok>\w+)/$',CheckResearchProject), 

    url(r'^createPaper/$',createPaper),
    url(r'^paper/(?P<id>\w+)/$',app.views.paper),
    url(r'^PaperIndex/$',app.views.paperIndex),
    url(r'^createCompetition/$',createCompetition),
    url(r'^competition/(?P<id>\w+)/$',app.views.competition),
    url(r'^CompetitionIndex/$',app.views.competitionIndex),
    url(r'^createExchange/$',createExchange), 
    url(r'^exchange/(?P<id>\w+)/$',app.views.exchange),
    url(r'^ExchangeIndex/$',app.views.exchangeIndex),
    url(r'^createStudentCadre/$',createStudentCadre), 
    url(r'^studentCadre/(?P<id>\w+)/$',app.views.studentCadre),
    url(r'^StudentCadreIndex/$',app.views.studentCadreIndex),

    url(r'^createIdeologyConstruction/$',createIdeologyConstruction),
    url(r'^ideologyConstruction/(?P<id>\w+)/$',ideologyConstruction),
    url(r'^IdeologyConstructionDetail/(?P<id>\w+)/$',IdeologyConstructionDetail), 
    url(r'^IdeologyConstructionIndex/$',IdeologyConstructionIndex), 

    url(r'^JoinIdeologyConstruction/(?P<id>\w+)/$',JoinIdeologyConstruction),
    url(r'^IdeologyConstructionSDetail/(?P<id>\w+)/$',app.views.IdeologyConstructionSDetail), 
    url(r'^CheckIdeologyConstruction/(?P<id>\w+)/(?P<isok>\w+)/$',app.views.CheckIdeologyConstruction),  
    url(r'^IdeologyConstructionList/$',app.views.ResearchProjectList), 
    url(r'^createLecture/$',createLecture),
    url(r'^lecture/(?P<id>\w+)/$',lecture),
    url(r'^LectureDetail/(?P<id>\w+)/$',LectureDetail), 
    url(r'^LectureIndex/$',LectureIndex), 
    url(r'^JoinLecture/(?P<id>\w+)/$',JoinLecture), 

    url(r'^createVolunteering/$',createVolunteering),
    url(r'^volunteering/(?P<id>\w+)/$',volunteering),
    url(r'^VolunteeringDetail/(?P<id>\w+)/$',VolunteeringDetail), 
    url(r'^VolunteeringIndex/$',VolunteeringIndex),
    url(r'^VolunteeringList/$',app.views.VolunteeringList), 
    url(r'^VolunteeringSDetail/(?P<id>\w+)/$',app.views.VolunteeringSDetail), 
    url(r'^CheckVolunteering/(?P<id>\w+)/(?P<isok>\w+)/$',app.views.CheckVolunteeringx),  
    url(r'^JoinVolunteering/(?P<id>\w+)/$',JoinVolunteering), 

    url(r'^createSchoolActivity/$',createSchoolActivity),
    url(r'^schoolActivity/(?P<id>\w+)/$',schoolActivity),
    url(r'^SchoolActivityDetail/(?P<id>\w+)/$',SchoolActivityDetail), 
    url(r'^SchoolActivityIndex/$',SchoolActivityIndex),
    url(r'^CheckSchoolActivity/(?P<id>\w+)/(?P<isok>\w+)/$',app.views.CheckSchoolActivityx),  
    url(r'^SchoolActivityList/$',app.views.SchoolActivityList),  
    url(r'^SchoolActivitySDetail/(?P<id>\w+)/$',app.views.SchoolActivitySDetail), 
    url(r'^JoinSchoolActivity/(?P<id>\w+)/$',JoinSchoolActivity),  

    url(r'^createInternship/$',createInternship), 
    url(r'^internship/(?P<id>\w+)/$',internship),
    url(r'^InternshipDetail/(?P<id>\w+)/$',InternshipDetail), 
    url(r'^InternshipIndex/$',app.views.InternshipIndex), 
    url(r'^InternshipList/$',app.views.InternshipList),  
    url(r'^CheckInternship/(?P<id>\w+)/(?P<isok>\w+)/$',app.views.CheckInternship),  
    url(r'^InternshipSDetail/(?P<id>\w+)/$',app.views.InternshipSDetail), 
    url(r'^JoinInternship/(?P<id>\w+)/$',JoinInternship),  

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
