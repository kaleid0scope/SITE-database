import app
from app.parameter import *
from app.models import *
from app.forms import *
from app.create import *
from exceptions import NameError

def getModel(str):
    ModelDic = {
        'User': User,
        'ResearchProjectRank': ResearchProjectRank,
        'IdeologyConstructionRank': IdeologyConstructionRank, 
        'LectureRank':LectureRank,
        'VolunteeringRank':VolunteeringRank,
        'SchoolActivityRank':SchoolActivityRank,
        'PaperRank':PaperRank,
        'CompetitionRank':CompetitionRank,
        'ExchangeRank':ExchangeRank,
        'StudentCadreRank':StudentCadreRank,
        'InternshipRank':InternshipRank,

        'ResearchProject': ResearchProjectRank,
        'IdeologyConstruction': IdeologyConstructionRank, 
        'Lecture':LectureRank,
        'Volunteering':VolunteeringRank,
        'SchoolActivity':SchoolActivityRank,
        'Paper':PaperRank,
        'Competition':CompetitionRank,
        'Exchange':ExchangeRank,
        'StudentCadre':StudentCadreRank,
        'Internship':InternshipRank,
    }
    return ModelDic.get(str, NameError)

def getForm(str):
    FormDic = {
        'Project':app.forms.ProjectForm,

        'ResearchProjectRank': app.forms.CreateResearchProjectForm,
        'IdeologyConstructionRank':app.forms.CreateIdeologyConstructionForm, 
        'LectureRank':app.forms.CreateLectureForm,
        'VolunteeringRank':app.forms.CreateVolunteeringForm,
        'SchoolActivityRank':app.forms.CreateSchoolActivityForm,
        'PaperRank':app.forms.CreatePaperForm,
        'CompetitionRank':app.forms.CreateCompetitionForm,
        'ExchangeRank':app.forms.CreateExchangeForm,
        'StudentCadreRank':app.forms.CreateStudentCadreForm,
        'InternshipRank':app.forms.CreateInternshipForm,

        'ResearchProject':app.forms.CreateResearchProjectForm,
        'IdeologyConstruction':app.forms.CreateIdeologyConstructionForm, 
        'Lecture':app.forms.CreateLectureForm,
        'Volunteering':app.forms.CreateVolunteeringForm,
        'SchoolActivity':app.forms.CreateSchoolActivityForm,
        'Paper':app.forms.CreatePaperForm,
        'Competition':app.forms.CreateCompetitionForm,
        'Exchange':app.forms.CreateExchangeForm,
        'StudentCadre':app.forms.CreateStudentCadreForm,
        'Internship':app.forms.CreateInternshipForm,

        'CreateResearchProjectRank':app.forms.CreateResearchProjectForm,
        'CreateIdeologyConstructionRank':app.forms.CreateIdeologyConstructionForm, 
        'CreateLectureRank':app.forms.CreateLectureForm,
        'CreateVolunteeringRank':app.forms.CreateVolunteeringForm,
        'CreateSchoolActivityRank':app.forms.CreateSchoolActivityForm,
        'CreatePaperRank':app.forms.CreatePaperForm,
        'CreateCompetitionRank':app.forms.CreateCompetitionForm,
        'CreateExchangeRank':app.forms.CreateExchangeForm,
        'CreateStudentCadreRank':app.forms.CreateStudentCadreForm,
        'CreateInternshipRank':app.forms.CreateInternshipForm,

        'CreateResearchProject':app.forms.CreateResearchProjectForm,
        'CreateIdeologyConstruction':app.forms.CreateIdeologyConstructionForm, 
        'CreateLecture':app.forms.CreateLectureForm,
        'CreateVolunteering':app.forms.CreateVolunteeringForm,
        'CreateSchoolActivity':app.forms.CreateSchoolActivityForm,
        'CreatePaper':app.forms.CreatePaperForm,
        'CreateCompetition':app.forms.CreateCompetitionForm,
        'CreateExchange':app.forms.CreateExchangeForm,
        'CreateStudentCadre':app.forms.CreateStudentCadreForm,
        'CreateInternship':app.forms.CreateInternshipForm,
    }
    return FormDic.get(str, NameError)

def getView(str):
    ViewDic = {
        'ResearchProjectRank':app.create.createResearchProject,
        'IdeologyConstructionRank': app.create.createIdeologyConstruction, 
        'LectureRank':app.create.createLecture,
        'VolunteeringRank':app.create.createVolunteering,
        'SchoolActivityRank':app.create.createSchoolActivity,
        'PaperRank':app.create.createPaper,
        'CompetitionRank':app.create.createCompetition,
        'ExchangeRank':app.create.createExchange,
        'StudentCadreRank':app.create.createStudentCadre,
        'InternshipRank':app.create.createInternship,
}
    return ViewDic.get(str, NameError)

def getType(request):
    return user_parameter(request)['type']

def refresh(request,url):
    assert isinstance(request, HttpRequest)
    return render(request,'refresh.html',{'url':url})
