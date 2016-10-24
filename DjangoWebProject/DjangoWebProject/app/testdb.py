# -*- coding: utf-8 -*-

from django.http import HttpResponse
from app.models import Inspectors

def testdb(request):
	insp1 = Inspectors(inspectorNum=10001,name='gong')
	insp1.save()
	return HttpResponse("<p>ok</p>")