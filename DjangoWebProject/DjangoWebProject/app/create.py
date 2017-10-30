# -*- coding: utf-8 -*-
import app
from app.models import *
from app.forms import *
from django.shortcuts import *

def createIdeologyConstruction(request,is_active = None): 
        form = app.forms.CreateIdeologyConstructionForm(request.POST)
        if form.is_valid():
                cd = form.cleaned_data
                project = IdeologyConstructionRank(
                                active = 0 if is_active == None else 1,
                                rankName = cd['ProjectName'],
                                startingTime = cd['startingTime'],
                                type = cd['type'],
                                Location = cd['Location'],
                                organizer = cd['organizer'],
                                Content = cd['Content'],)
                return project
        else: return None

def createPaper(request,is_active = None):#active:应该是 是否通过审批
        form = app.forms.CreatePaperForm(request.POST)
        if form.is_valid():
                cd = form.cleaned_data
                project = PaperRank(rankName = cd['ProjectName'],
                                journalName = cd['JournalName'],
                                startingTime = cd['ProjectTime'],
                                AuthorRanking = cd['AuthorRanking'],
                                rank = cd['Rank'],
                                active = 0 if is_active == None else 1,
                                )
                return project
        else: return None

def createCompetition(request,is_active = None):
        form = app.forms.CreateCompetitionForm(request.POST)
        if form.is_valid():
                cd = form.cleaned_data
                project = CompetitionRank(rankName = cd['ProjectName'],
                                startingTime = cd['ProjectTime'],
                                active = 0 if is_active == None else 1,
                                Level = cd['level'],
                                rank = cd['rank'],)
                return project
        else: return None
def createStudentCadre(request,is_active = None):
        form = app.forms.CreateStudentCadreForm(request.POST)
        if form.is_valid():
                cd = form.cleaned_data
                project = StudentCadreRank(rankName = cd['rankName'],
                                organizitionType = cd['organizitionType'],
                                organizitionName = cd['organizitionName'],
                                active = 0 if is_active == None else 1,
                               )
                return project
        else: return None
def createExchange(request,is_active = None):
        form = app.forms.CreateExchangeForm(request.POST)
        if form.is_valid():
                cd = form.cleaned_data
                project = ExchangeRank(rankName = cd['ProjectName'],
                                type = cd['type'],
                                nature = cd['nature'],
                                startTime = cd['startTime'],
                                endTime = cd['endTime'],
                                active = 0 if is_active == None else 1,
                               )
                return project
        else: return None
def createInternship(request,is_active = None): 
        form = app.forms.CreateInternshipForm(request.POST)
        if form.is_valid():
                cd = form.cleaned_data
                project = InternshipRank(
                                active = 0 if is_active == None else 1,
                                rankName = cd['ProjectName'],
                                Time = cd['startingTime'],
                                type = cd['type'],
                                Location = cd['Location'],
                                job = cd['Job'],
                                contribution = cd['Contribution'],
                                report = cd['Report'],
                                appraisal = cd['Appraisal'])
                return project
        else: return None
def createResearchProject(request,is_active = None):
        form = app.forms.CreateResearchProjectForm(request.POST)
        if form.is_valid():
                cd = form.cleaned_data
                project = ResearchProjectRank(
active = 0 if is_active == None else 1,rankName = cd['ProjectName'],startingTime = cd['ProjectTime'],role = cd['Role'],rank = cd['Rank'],)
                return project
        else: return None
def createLecture(request,is_active = None):
        form = app.forms.CreateLectureForm(request.POST)
        if form.is_valid():
                cd = form.cleaned_data
                project = LectureRank(rankName = cd['ProjectName'],
                                type = cd['type'],
                                active = 0 if is_active == None else 1,
                                startingTime = cd['startingTime'],
                                organizer = cd['organizer'],
                                speaker = cd['speaker'],
                                Location = cd['Location'],
                                Content = cd['Content'],)
                return project
        else: return None
def createVolunteering(request,is_active = None):
        form = app.forms.CreateVolunteeringForm(request.POST)
        if form.is_valid():
                cd = form.cleaned_data
                project = VolunteeringRank(rankName = cd['ProjectName'],
                                startingTime = cd['startingTime'],
                                volunteerTime = cd['volunteerTime'],
                                organizer = cd['organizer'],
                                Location = cd['Location'],
                                Content = cd['Content'],
                                active = 0 if is_active == None else 1,)
                return project
        else: return None
def createSchoolActivity(request,is_active = None):
        form = app.forms.CreateSchoolActivityForm(request.POST)
        if form.is_valid():
                cd = form.cleaned_data
                project = SchoolActivityRank(rankName = cd['ProjectName'],
                                startingTime = cd['startingTime'],
                                type = cd['type'],
                                sponsor = cd['sponsor'],
                                organizer = cd['organizer'],
                                awardLevel = cd['awardLevel'],
                                active = 0 if is_active == None else 1,)
                return project
        else: return None