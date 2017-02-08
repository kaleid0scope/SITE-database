from django.contrib import admin
import app.models
from app.models import Inspectors,Authorizations,ResearchProjectRank,ResearchProject,LectureRank,Lecture,ChoicesTeam,Choices
 
 
admin.site.register(Inspectors)
admin.site.register(Authorizations)
admin.site.register(ResearchProjectRank)
admin.site.register(ResearchProject)
admin.site.register(LectureRank)
admin.site.register(Lecture)
admin.site.register(Choices)
admin.site.register(ChoicesTeam)
admin.site.register(app.models.PaperRank)