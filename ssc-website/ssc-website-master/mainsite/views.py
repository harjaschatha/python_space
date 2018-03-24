from django.views.decorators.http import require_http_methods
from django.shortcuts import render,get_object_or_404,redirect
from django.forms.models import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.http import Http404
import mainsite,office,stephens,attendance
from mainsite.functions import *
from django.contrib.auth.models import User,Group


def home(request):
	'''
	Returns the homepage of the college website.
	Gives basic informatino and acts as an index for the site.
	
	-------------------------------------------
	Provides top 5 notification objects including pinned objects.=notification
	Provides top 5 principal desk objects.=principal_desk
	Provides Slideshow picture objects.Get url for photo by {{<object>.associated_photo.url}} in template=slideshow
	-------------------------------------------
	
	'''
	data={}
	data['domain_name']=stephens.settings.domain_name
	data['slideshow']=mainsite.models.home_slideshow_photo.objects.all()
	notice_category=mainsite.models.notification_category.objects.all()
	notice,princi=None,None
	for i in notice_category:
		if 'principal' in i.name.replace(' ','').lower().strip():
			princi=i
		if 'notice' in i.name.replace(' ','').lower().strip():
			if 'admission' not in i.name.replace(' ','').lower().strip():
				notice=i
	data['notification']=mainsite.models.notification.objects.filter(category=notice).order_by('pinned','-publish_date','-pk')[:5]
	data['principal_desk']=mainsite.models.notification.objects.filter(category=princi).order_by('-publish_date','-pk')[:5]
	return render(request,'mainsite/home.html',data)
	
def notice_home(request):
	'''
	shows all notices which are currently active and issued.
	
	--------------------------------------------
	Provides a list of notice objects.=notifications
	--------------------------------------------
	'''
	data={}
	data['domain_name']=stephens.settings.domain_name
	notice,princi=None,None
	notice_category=mainsite.models.notification_category.objects.all()
	for i in notice_category:
		if 'principal' in i.name.replace(' ','').lower().strip():
			princi=i
		if 'notice' in i.name.replace(' ','').lower().strip():
			if 'admission' not in i.name.replace(' ','').lower().strip():
				notice=i
	data['notifications']=mainsite.models.notification.objects.filter(category=notice).order_by('-publish_date','pinned')
	return render(request,'mainsite/notice_home.html',data)
def notice_detail(request,cid):
	'''
	shows details of a notice
	'''
	data={}
	template='mainsite/notice_detail.html'
	notification=get_object_or_404(mainsite.models.notification,pk=cid)
	data['slots']=mainsite.models.Slot.objects.filter(notif=notification).order_by('order')
	data['notice']=notification
	return render(request,template,data)
	
def principal_home(request):
	'''
	shows all notices which are currently active and issued by the principal
	
	--------------------------------------------
	Provides a list of notice objects.=notification
	--------------------------------------------
	'''
	data={}
	data['domain_name']=stephens.settings.domain_name
	notice,princi=None,None
	notice_category=mainsite.models.notification_category.objects.all()
	for i in notice_category:
		if 'principal' in i.name.replace(' ','').lower().strip():
			princi=i
		if 'notice' in i.name.replace(' ','').lower().strip():
			if 'admission' not in i.name.replace(' ','').lower().strip():
				notice=i
	data['notifications']=mainsite.models.notification.objects.filter(category=princi).order_by('-publish_date','pinned')
	return render(request,'mainsite/notice_home.html',data)


def admission(request):
	'''
	Returns the homepage for admissions.
	Gives information on past,present,future admissions.
	refers to academics page for course and faculty details.
	-------------------------------------------
	Provides nothing so far.
	
	-------------------------------------------
	'''
	data={}
	data['domain_name']=stephens.settings.domain_name
	return render(request,'mainsite/admission.html',data)
def academics(request):
	'''
	Returns homepage of the academics section.
	Gives information on courses,faculty etc. Everything related to academics.
	-------------------------------------------
	Provides all active members of the faculty group.list of user objects=faculty
	Provides list of courses in the college.List of course objects.=courses
	-------------------------------------------
	'''
	data={}
	data['domain_name']=stephens.settings.domain_name
	data['faculty']=office.models.faculty.objects.all()
	data['courses']=office.models.course.objects.all()
	return render(request,'mainsite/academics.html',data)
	
def society(request):
	data={}
	data['domain_name']=stephens.settings.domain_name
	data['societies']=office.models.deptsoc.objects.filter(is_society=True)
	return render(request,'mainsite/society.html',data)
def society_detail(request,nick):
	'''
	returns named society
	'''
	data={}
	obj=get_object_or_404(office.models.deptsoc,nickname=nick)
	data['society']=obj
	return render(request,'mainsite/society.html',data)
def department(request):
	data={}
	data['domain_name']=stephens.settings.domain_name
	data['departments']=office.models.deptsoc.objects.filter(is_society=False)
	return render(request,'mainsite/department.html',data)
def department_detail(request,nick):
	'''
	department details
	'''
	data={}
	dept=get_object_or_404(office.models.deptsoc,nickname=nick)
	data['department']=office.models.faculty.objects.filter(dept=dept)
	return render(request,'mainsite/department.html',data)
	
def archive(request):
	data={}
	data['domain_name']=stephens.settings.domain_name
	return render(request,'mainsite/society.html',data)
def alumni(request):
	data={}
	data['domain_name']=stephens.settings.domain_name
	return render(request,'mainsite/alumni.html',data)
def contact(request):
	data={}
	data['domain_name']=stephens.settings.domain_name
	return render(request,'mainsite/contact.html',data)

@login_required
@require_http_methods(['POST'])
def profile_upload(request,nick):
	form=mainsite.models.faculty_upload_form(request.POST,request.FILES)
	if form.is_valid():
		upl=form.save(commit=False)
		#get the current faculty logged in
		fac=get_profile(nick)#from mainsite common functions
		if fac.user!=request.user:#if not authenticated
			raise Http404
		upl.uploaded_by=fac
		upl.save()
	return redirect('profile_detail',args=[request.user.profile.nickname])
		
def profile_detail(request,nick=None):
	''' Profile of a person '''
	data={}
	
	#-------------------------------------------------get profile
	if nick==None:
		if request.user.is_authenticated():
			nick=request.user.profile.nickname
		else:
			raise Http404
		return redirect('profile_detail',nick)
	data['profile'],student_flag=get_profile(nick)#from mainsite common functions
	#---------------------------------------------------profile obtained or error raised
	data['student_flag']=student_flag
	#if everything goes on well person is found
	if not student_flag:#profile is of a faculty
		uploads=mainsite.models.faculty_uploads.objects.filter(uploaded_by=data['profile'])
		data['uploads']=uploads
		data['upload_form']=mainsite.models.faculty_upload_form()
	#handle the request types
	if request.method=='GET':
		template='mainsite/profile.html'
	if request.method=='POST':
		pass#updating profile details
	return render(request,template,data)

@require_http_methods(['POST'])
def profile_contact(request,nick):
	data={}
	#-------------------------------------------------get profile
	data['profile'],student_flag=get_profile(nick)#from mainsite common functions
	#---------------------------------------------------profile obtained or error raised
	if request.method=='POST':
	 	#get relevent data
		email_to=data['profile'].user.email
		email_from=request.POST['from']
		subject=request.POST['subject']
		message=request.POST['message']
		#try to send message
		try:
			contact_notification(email_from,email_to,subject,message)
		except:
			data['status']='Your message was not sent due to an error with our email services.'
		else:
			data['status']='Your message has been sent successfully to the email provided by the current profile'
		#set the new template
		template='mainsite/message_sent.html'
	return render(request,template,data)
def course_detail(request,cid):
	'''course details'''
	data={}
	data['course']=get_object_or_404(office.models.course,pk=cid)
	data['papers']=office.models.paper.objects.filter(course=data['course'])
	return render(request,'mainsite/course.html',data)
