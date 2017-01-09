from django.contrib import admin
from app.models import Inspectors,Students,Authorizations,ResearchProjectRank,ResearchProject,LectureRank,Lecture,ChoicesTeam,Choices
 
 
admin.site.register(Inspectors)
admin.site.register(Students)
admin.site.register(Authorizations)
admin.site.register(ResearchProjectRank)
admin.site.register(ResearchProject)
admin.site.register(LectureRank)
admin.site.register(Lecture)
admin.site.register(Choices)
admin.site.register(ChoicesTeam)