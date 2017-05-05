from app.parameter import *
from app.models import *
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
        'Project':ProjectForm,

        'ResearchProjectRank': CreateResearchProjectForm,
        'IdeologyConstructionRank':CreateIdeologyConstructionForm, 
        'LectureRank':CreateLectureForm,
        'VolunteeringRank':CreateVolunteeringForm,
        'SchoolActivityRank':CreateSchoolActivityForm,
        'PaperRank':CreatePaperForm,
        'CompetitionRank':CreateCompetitionForm,
        'ExchangeRank':CreateExchangeForm,
        'StudentCadreRank':CreateStudentCadreForm,
        'InternshipRank':CreateInternshipForm,

        'ResearchProject':CreateResearchProjectForm,
        'IdeologyConstruction':CreateIdeologyConstructionForm, 
        'Lecture':CreateLectureForm,
        'Volunteering':CreateVolunteeringForm,
        'SchoolActivity':CreateSchoolActivityForm,
        'Paper':CreatePaperForm,
        'Competition':CreateCompetitionForm,
        'Exchange':CreateExchangeForm,
        'StudentCadre':CreateStudentCadreForm,
        'Internship':CreateInternshipForm,

        'CreateResearchProjectRank': CreateResearchProjectForm,
        'CreateIdeologyConstructionRank':CreateIdeologyConstructionForm, 
        'CreateLectureRank':CreateLectureForm,
        'CreateVolunteeringRank':CreateVolunteeringForm,
        'CreateSchoolActivityRank':CreateSchoolActivityForm,
        'CreatePaperRank':CreatePaperForm,
        'CreateCompetitionRank':CreateCompetitionForm,
        'CreateExchangeRank':CreateExchangeForm,
        'CreateStudentCadreRank':CreateStudentCadreForm,
        'CreateInternshipRank':CreateInternshipForm,

        'CreateResearchProject': CreateResearchProjectForm,
        'CreateIdeologyConstruction':CreateIdeologyConstructionForm, 
        'CreateLecture':CreateLectureForm,
        'CreateVolunteering':CreateVolunteeringForm,
        'CreateSchoolActivity':CreateSchoolActivityForm,
        'CreatePaper':CreatePaperForm,
        'CreateCompetition':CreateCompetitionForm,
        'CreateExchange':CreateExchangeForm,
        'CreateStudentCadre':CreateStudentCadreForm,
        'CreateInternship':CreateInternshipForm,
    }
    return FormDic.get(str, NameError)

def getView(str):
    ViewDic = {
        'ResearchProjectRank': createResearchProject,
        'IdeologyConstructionRank': createIdeologyConstruction, 
        'LectureRank':createLecture,
        'VolunteeringRank':createVolunteering,
        'SchoolActivityRank':createSchoolActivity,
        'PaperRank':createPaper,
        'CompetitionRank':createCompetition,
        'ExchangeRank':createExchange,
        'StudentCadreRank':createStudentCadre,
        'InternshipRank':createInternship,
}

def getType(request):
    return user_parameter(request)['type']

def refresh(request,url):
    assert isinstance(request, HttpRequest)
    return render(request,'refresh.html',{'url':url})
