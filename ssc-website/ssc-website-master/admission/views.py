from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from django.http import Http404
from stephens.common_functions import *
import admission,stephens,mainsite

def home(request):
	'''
	admissions homepage.
	Try to implement as a flatpage...
	'''
	data={}
	data['control']=admission.models.admission_control.objects.first()
	return render(request,'admission/home.html',data)
def procedure(request):
	'''
	view defines the procedure for admission
	To be flatpaged....
	'''
	data={}
	return render(request,'admission/procedure.html',data)
def dates(request):
	'''
	returns important dates related to admissions
	-------------------------------
	Provides a list of dates object=dates
	-------------------------------
	'''
	data={}
	data['dates']=admission.models.dates.objects.filter(valid_upto__gte=timezone.now())
	return render(request,'admission/dates.html',data)
def notice(request):
	'''
	notices regarding admissions
	----------------------------------
	Provides a list of notices=notices
	----------------------------------
	'''
	data={}
	data['domain_name']=stephens.settings.domain_name
	categ=mainsite.models.notification_category.objects.all()[2]
	data['notices']=mainsite.models.notification.objects.filter(category=categ).filter(publish_date__lte=timezone.now())
	return render(request,'admission/notices.html',data)
def cutoff(request):
	'''
	cutoffs of this year
	-------------------------------------
	Provides a list of category cutoffs=cutoffs
	Provides a list of subjects and their cutoff validation dates=courses
	-------------------------------------
	'''
	data={}
	data['courses']=admission.models.cutoff_subject.objects.all()
	data['cutoffs']=admission.models.category_cutoff.objects.filter(cutoff_subject__valid_upto__gte=timezone.now()).order_by('cutoff_subject','category')
	return render(request,'admission/cutoff.html',data)
	
def result(request):
	'''
	results of this and previous years
	-------------------------------------
	Provides a list of admitted candidates=admitted
	-------------------------------------
	'''
	data={}
	data['admitted']=admission.models.admission_candidate.objects.filter(cutoff_status=True,admitted=True)
	return render(request,'admission/result.html',data)
	
def faq(request):
	'''
	returns the frequently asked questions with answers.
	User can ask a new question.
	-------------------------------------
	Provides a list of q_a objects=q_a
	-------------------------------------
	'''
	data={}
	data['q_a']=admission.models.q_a.objects.order_by('rank')
	return render(request,'admission/faq.html',data)
def admission_form(request):
	'''
	admission_form
	----------------------
	Provides an admission_form=form
	'''
	if request.method=='GET':
		data={}
		if admission.models.admission_control.objects.first().accept_admission_forms:
			data['form']=admission.models.admission_form()
		return render(request,'admission/form.html',data)
	if request.method=='POST':
		data={}
		if admission.models.admission_control.objects.first().accept_admission_forms:		
			form=admission.models.admission_form(request.POST,request.FILES)
			if form.is_valid():
				admission_candidate=form.save()
				data['candidate']=admission_candidate
				try:
					admission_registration(data['candidate'].email)
				except Exception as e:
					print e
					return render(request,'admission/email_down.html')
				else:			
						return render(request,'admission/successful.html',data)
			else:
				data['form']=form
				return render(request,'admission/form.html',data)
		else:
			return render(request,'admission/form.html',data)
def candidate_detail(request,cid):
	'''
	provides details of a candidate's admission form
	for reference
	'''
	if type(cid)!=type(0):
		try:
			cid=int(cid)#convert if not of same type
		except Exception as e:
			print e
			raise Http404
	data={}
	data['candidate']=get_object_or_404(admission.models.admission_candidate,pk=cid)
	return render(request,'admission/detail.html',data)
def resend_confirmation(request,cid) :
	data={}
	if admission.models.admission_control.objects.first().accept_admission_forms:
		data['candidate']=get_object_or_404(admission.models.admission_candidate,pk=cid)
		try:
			admission_registration(data['candidate'].email)
		except Exception as e:
			print e
			return render(request,'admission/email_down.html')
		else:
			return render(request,'admission/successful.html',data) 
	else:
		return render(request,'admission/form.html',data)
