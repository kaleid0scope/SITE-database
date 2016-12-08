from django.contrib import admin
from app.models import Inspectors 
from app.models import Students 
from app.models import Projects
from app.models import Teachers
 
 
admin.site.register(Inspectors)
admin.site.register(Students)
admin.site.register(Projects)
admin.site.register(Teachers)