"""
Definition of models.
"""

from django.db import models

# Create your models here.

class Inspectors(models.Model):
    inspectorID = models.PositiveIntegerField()
    name = models.CharField(max_length = 20)

class Students(models.Model):
    StudentID =models.PositiveIntegerField()
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