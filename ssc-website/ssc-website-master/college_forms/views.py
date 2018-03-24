from django.shortcuts import render
from college_forms.models import admission_form



def home(request):
	'''
	Shows the available forms
	'''
	data={}
	data['forms']=None
	return render(request,'college_forms/home.html',data)

