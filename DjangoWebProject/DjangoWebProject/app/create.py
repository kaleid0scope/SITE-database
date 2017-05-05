# -*- coding: utf-8 -*-
from app.models import *
from app.forms import *
from django.shortcuts import *

def createIdeologyConstruction(request,student): 
        form = CreateIdeologyConstructionForm(request.POST)
        if form.is_valid():
                cd = form.cleaned_data
                project = IdeologyConstructionRank(teacher = student,
                                status = '待审核',
                                rankName = cd['ProjectName'],
                                startingTime = cd['startingTime'],
                                type = cd['type'],
                                Location = cd['Location'],
                                organizer = cd['organizer'],
                                Content = cd['Content'],
                                SupportText = cd['SupportText'])
                return project
def createPaper(request,student):
        form = CreatePaperForm(request.POST)
        if form.is_valid():
            #try:
                cd = form.cleaned_data
                project = PaperRank(rankName = cd['ProjectName'],
                                journalName = cd['JournalName'],
                                student = student,
                                startingTime = cd['ProjectTime'],
                                AuthorRanking = cd['AuthorRanking'],
                                status = '待审核',
                                rank = '',
                                )
                return project
def createCompetition(request,student):
        form = CreateCompetitionForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = CompetitionRank(rankName = cd['ProjectName'],
                                student = student,
                                startingTime = cd['ProjectTime'],
                                status = '待审核',
                                level = cd['level'],
                                rank = cd['rank'],)
                return project
def createStudentCadre(request,student):
        form = CreateStudentCadreForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = StudentCadreRank(teacher = student,
                                organizitionType = cd['organizitionType'],
                                organizitionName = cd['organizitionName'],
                                status = '待审核',
                               )
                return project
def createExchange(request,student):#待修改
        form = CreateExchangeForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = ExchangeRank(rankName = cd['ProjectName'],
                                type = cd['type'],
                                nature = cd['nature'],
                                student = student,
                                startTime = cd['startTime'],
                                endTime = cd['endTime'],
                                status = '待审核',
                               )
                return project
def createResearchProject(request,student):
        form = CreateResearchProjectForm(request.POST)
        if form.is_valid():
            #try:
                cd = form.cleaned_data
                project = ResearchProjectRank(rankName = cd['ProjectName'],teacher = student,startingTime = cd['ProjectTime'],status = '待审核',rank = '',)
                return project
def createLecture(request,student):
        form = CreateLectureForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = LectureRank(rankName = cd['ProjectName'],
                                type = cd['type'],
                                teacher = student,
                                startingTime = cd['startingTime'],
                                organizer = cd['organizer'],
                                speaker = cd['speaker'],
                                Location = cd['Location'],
                                Content = cd['Content'],
                                status = '待审核')
                return project
def createVolunteering(request,student):
        form = CreateVolunteeringForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = VolunteeringRank(rankName = cd['ProjectName'],
                                teacher = Students.objects.get(user = request.user),
                                startingTime = cd['startingTime'],
                                volunteerTime = cd['volunteerTime'],
                                organizer = cd['organizer'],
                                Location = cd['Location'],
                                Content = cd['Content'],
                                status = '待审核')
                return project
def createSchoolActivity(request,student):
        form = CreateSchoolActivityForm(request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                project = SchoolActivityRank(rankName = cd['ProjectName'],
                                teacher = student,
                                startingTime = cd['startingTime'],
                                type = cd['type'],
                                sponsor = cd['sponsor'],
                                organizer = cd['organizer'],
                                awardLevel = cd['awardLevel'],
                                status = '待审核')
                return project