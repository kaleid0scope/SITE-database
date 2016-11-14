"""
Definition of models.
"""

from django.db import models

# Create your models here.

class Inspectors(models.Model):
    inspectorNum = models.PositiveIntegerField()
    name = models.CharField(max_length = 20)

class Students(models.Model):
    StudentNum =models.PositiveIntegerField()
    name = models.CharField(max_length = 20)
    sex =models.BooleanField()
    year = models.PositiveSmallIntegerField()
    phone = models.PositiveIntegerField()
    email = models.EmailField()
    photo = models.URLField()
    born = models.DateField()
    root = models.CharField(max_length = 50)
    nation = models.CharField(max_length = 50)
    politicalStatus = models.CharField(max_length = 50)
    location = models.CharField(max_length = 50)
    identityType = models.CharField(max_length = 20)
    identityNumber = models.PositiveIntegerField()
    speciality = models.CharField(max_length = 50)
    source = models.CharField(max_length = 50)
    collegeEntranceExaminationScore = models.PositiveSmallIntegerField()
    inspector = models.ForeignKey(Inspectors)

class Teachers(models.Model):
    teacherNum = models.IntegerField()
    name = models.CharField(max_length = 20)
    sex =models.BooleanField()

class Projects(models.Model):
    name = models.CharField(max_length = 20)
    number = models.SmallIntegerField()
    teacher = models.ForeignKey(Teachers)
    Location = models.CharField(max_length = 50)

class Relation(models.Model):
    project = models.ForeignKey(Projects)
    student = models.ForeignKey(Students)

class Pig(models.Model):
    pigid = models.IntegerField(primary_key = True,db_column = "ID")
    pigname = models.CharField(max_length = 20)
    
