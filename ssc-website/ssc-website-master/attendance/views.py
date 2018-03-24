from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory,inlineformset_factory
import json
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import attendance,office
from django.utils import timezone
from attendance import functions

def home(request):
	'''Homepage for attendance.
	Gives a search function to select students by course and semester
	-----------------GET-----------------
	Provides a list of courses=courses
	Provides a list of semesters=semesters
	----------------POST----------------
	Provides a list of students for given course and semester=students
	OR
	Provides an error variable
	
	JSON Formatted
	
	'''
	data={}
	
	if request.method=='GET':#simple http page
		data['courses']=office.models.course.objects.all()
		data['semesters']=[1,2,3,4,5,6]
		return render(request,'attendance/home.html',data)
	if request.method=='POST':#form submission
		#see if the course,semester exists
		try:
			course=office.models.course.objects.get(pk=request.POST['course'])
			semester=request.POST['semester']
		except Exception as e:
			print e#print the exception encountered
		else:#if course exists
			try:
				#get all students of that course in that semester
				students=office.models.student.objects.filter(course=course).filter(current_semester=semester)
				stu=[]
				#compose the student list
				for i in students:
					x={}
					x['name']=i.user.first_name.replace('_',' ').capitalize() + ' ' + i.user.last_name.capitalize()
					x['id']=i.id
					stu.append(x)
			except Exception as e:
				print e#debug output
		#return the data
		return HttpResponse(json.dumps(stu),content_type='application/json')
def student_id(request,studentid):
	'''Attendance
	for a student
	----------------------
	Provides attendance for student=student_attendance
	if student does not exist provides an error message
	----------------------
	'''
	data={}
	
	try:
		stud=office.models.student.objects.get(pk=studentid)
	except Exception as e:
		print e
		data['error']='Student Does not exist'
	else:
		data['student_attendance']=attendance.models.student_attendance.objects.filter(student=stud)
	return render(request,'attendance/student.html',data)
	
@login_required
def ECA_list(request):
	data={}
	template='attendance/eca_list.html'
	#check if user is active yet
	if request.user.is_active:
		#check if user is a student
		try:
			student=office.models.student.objects.get(user=request.user)
		except Exception as e:
			print '------'
			print e
			print '------'
			data['not_authentic']='Not a student'
		else:
			#get eca models
			data['eca_requests']=attendance.models.eca_request.objects.filter(stud=student).order_by('pk')
			#need to get logs
	else:
		data['not_authentic']='Not an active user.Contact Administration.'
	return render(request,template,data)
@login_required
def ECA_sign(request):
	"Portal for signing ECAs." 
	data={} 
	template='attendance/eca_sign.html' 
	#generate form factory
	factory=modelformset_factory(attendance.models.eca_request,extra=0,exclude=['approved'],can_delete=False)
	user=request.user
	if request.method=='GET':
		unsigned=functions.get_unsigned_eca_requests(user)
		if unsigned!=None:
			data['formset']=factory(queryset=unsigned)
			data['status']='You have unsigned ECA requests.'
		else:
			data['status']='You have no ECA requests to sign.'
		return render(request,template,data)
	if request.method=='POST':
		unsigned=functions.get_unsigned_eca_requests(user)
		signed=factory(request.POST,queryset=unsigned)
		if signed.is_valid():
			fac=office.models.faculty.objects.get(user=user)
			signed.save()
			data['status']='Successfully signed ECA requests'
			data['formset']=factory(queryset=unsigned)
		else:
			data['formset']=signed
			data['status']='Your entries did not validate. Please resubmit'
		return render(request,template,data)
	data['status']='Something went wrong. If problem persists contact Website Admin'
	return render(request,template,data)
	
@login_required
def ECA_approve(request):
	'''Portal for ECA approval'''
	data={}
	template='attendance/eca_approve.html'
	factory=modelformset_factory(attendance.models.eca_request,extra=0,exclude=['approved'],can_delete=False)
	if request.method=='GET':
		user=request.user
		unsigned=functions.get_unapproved_eca_requests(user)
		if unsigned!=None:
			data['formset']=factory(queryset=unsigned)
			data['status']='You have unsigned ECA requests.'
		return render(request,template,data)
	if request.method=='POST':
		user=request.user
		unsigned=functions.get_unapproved_eca_requests(user)
		signed=factory(request.POST,queryset=unsigned)
		if signed.is_valid():
			fac=office.models.faculty.objects.get(user=user)
			signed.save()
			data['status']='Successfully signed ECA requests'
			data['formset']=factory(queryset=unsigned)
		else:
			data['formset']=signed
			data['status']='Your entries did not validate. Please resubmit'
		return render(request,template,data)
	data['status']='Something went wrong. If problem persists contact Website Admin'
	return render(request,template,data)
@login_required
def ECA_new(request):
	'''A form to request ECA from the college.
	-------GET--------
	Provides a form to define the dates during which ECA is required.
	------POST--------
	Creates a new ECA object from the POST data recieved
	'''
	data={}
	template='attendance/eca_new.html'
	#if user is active or not
	if request.user.is_active:
		#check if the user is a student and registered
		try:
			student=office.models.student.objects.get(user=request.user)
		except Exception as e:
			print '-----------'
			print e
			print '-----------'
			data['not_authentic']='You must be a student to submit ECA'
			#if not then return error
			return render(request,template,data)
		else:
			#make the dates formset
			formset=inlineformset_factory(attendance.models.eca_request,attendance.models.eca_date,extra=5,can_delete=False)
			if request.method=='GET':
				#return an empty form
				data['form']=formset(initial=[{'start':timezone.now()}])
				data['detail']=attendance.models.eca_request_form()
				data['status']='New ECA submission'
			if request.method=='POST':
				#print 'detail_form-------debug'
				#get the details for the eca request
				detail_form=attendance.models.eca_request_form(request.POST)
				if detail_form.is_valid():
					eca_details=detail_form.save(commit=False)
					eca_details.stud=office.models.student.objects.get(user=request.user)
					eca_details.save()
				else:
					#if not valid return the errors found
					data['detail']=detail_form
					return render(request,template,data)
				#print 'Detail  form done---------debug'
				dates=formset(request.POST,instance=eca_details)
				if dates.is_valid():
					dates.save()
					#print 'dates done------debug'
					data['status']='Successfully submitted ECA'
					data['form']=formset(initial=[{'start':timezone.now()}])
					data['detail']=attendance.models.eca_request_form()
					#return completed status
				else:
					data['detail']=detail_form
					data['form']=dates
	else:
		data['not_authentic']='Not logged in'
	return render(request,template,data)

def ECA_home(request):
	'''Returns the links of various ECA functinoalities based on student/faculty/anoonymous users'''
	data={}
	template='attendance/eca_home.html'
	user=request.user
	if user.is_authenticated():
		try:
			stu=office.models.student.objects.get(user=user)
		except:
			data['faculty']=True
		else:
			data['student']=True
	return render(request,template,data)
@login_required
def short_attendance(request,filter=2.0/3):
	'''Returns a list of students and their lecture and theory and practical attendances'''
	data={}
	template='attendance/short.html'
	attends=attendance.models.student_attendance.objects.all().order_by('student')
	attendances={}
	current_student=office.models.student.objects.first()
	cur_lec=0.0
	cur_tut=0.0
	cur_pr=0.0
	for stu_attd in attends:
		if stu_attd.student==current_student:
			#% stu_attd/(total-adjust) is added to existing
			cur_lec+=(float(stu_attd.lecture)/(stu_attd.class_attendance.lecture-stu_attd.a_lecture))*100.0
			cur_tut+=(float(stu_attd.tutorial)/(stu_attd.class_attendance.tutorial-stu_attd.a_tutorial))*100.0
			cur_pr+=(float(stu_attd.practical)/(stu_attd.class_attendance.practical-stu_attd.a_practical))*100.0
			#average of % is done
			cur_lec/=2.0
			cur_tut/=2.0
			cur_pr/=2.0
		else:
			#student has changed. Thus update the data in database
			attendances[current_student.__unicode__()]={'lecture':cur_lec,'tutorial':cur_tut,'practical':cur_pr}
			current_student=stu_attd.student
			#assign % attendance
			cur_lec=(stu_attd.lecture/float(stu_attd.class_attendance.lecture-stu_attd.a_lecture))*100.0
			cur_tut=(stu_attd.tutorial/float(stu_attd.class_attendance.tutorial-stu_attd.a_tutorial))*100.0
			cur_pr=(stu_attd.practical/float(stu_attd.class_attendance.practical-stu_attd.a_practical))*100.0
	data['attendance']=attendances
	return render(request,template,data)
@login_required
def class_attendance(request,paper_id):
	'''Returns the attendance for an entire class for the last/current month to 
	be edited. Only if logged in
	'''
	data={}
	template='attendance/class.html'
	paper=get_object_or_404(attendance.models.paper_attendance,pk=paper_id)
	stu_attd=attendance.models.student_attendance.objects.filter(class_attendance=paper)
	data['classid']=paper_id
	if request.method=='GET':
		if request.user==paper.taught_by.user:
			data['editable']=True
			pap=attendance.models.paper_attd_form(instance=paper)
			data['paper']=pap
			factory=modelformset_factory(attendance.models.student_attendance,extra=0,can_delete=False,form=attendance.models.stu_attd_form)
			qset=attendance.models.student_attendance.objects.filter(class_attendance=paper)
			data['students']=factory(queryset=qset)		
		else:
			data['paper']=paper
			data['stu_attd']=stu_attd
			data['editable']=False
		return render(request,template,data)
	if request.method=='POST':
		qset=attendance.models.student_attendance.objects.filter(class_attendance=paper)
		if request.user==paper.taught_by.user:#only if authorized
			factory=modelformset_factory(attendance.models.student_attendance,extra=0,can_delete=False,form=attendance.models.stu_attd_form)
			std=factory(request.POST,queryset=qset)
			if std.is_valid():
				std.save()
				print 'allok stu'
			else:
				data['paper']=pap
				data['students']=std
				print 'stu error'
				return render(request,template,data)
			return redirect('class_attendance',paper_id)
			
@login_required	
def class_attend_upd(request,paper_id):
	"paper_attendance_updates"
	if request.method=='POST':
		paper=get_object_or_404(attendance.models.paper_attendance,pk=paper_id)
		if request.user==paper.taught_by.user:#only if authorized
			pap=attendance.models.paper_attd_form(request.POST,instance=paper)
			if pap.is_valid():
				pap.save()
				return HttpResponse('Successful',content_type='application/json')
				print 'allok paper'
			else:
				print 'paper error'
		return HttpResponse('UnSuccessful',content_type='application/json')

