import os
import sys
import shutil
import random
import datetime
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stephens.settings")

from django.core.files import File

from django.contrib.auth.models import User,Group
from django.core.management import execute_from_command_line
from django.utils import timezone

def clean_to_string(string):
	'''
	removes non ascii characters
	'''
	allowed='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'#alphabets
	allowed+=allowed.lower()#lowercase
	allowed+='!@#$%^&*()_+=-.,: '
	allowed+="'"
	allowed+='\n'
	new_str=''
	for i in string:
		if i in allowed:
			new_str+=i
	return new_str
import mainsite,attendance,office,events,admission,college_forms
function_list=[]#a list of setup function to be run
SETUP_SUPPORT_FOLDER='setup_support'#where the setup data files are located
#------------------------------------------------------------------------------------------------
control=admission.models.admission_control()#enable form submission
control.accept_admission_forms=True
control.prospectus=File(file(os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,'prospectus.pdf')))
control.save()
#------------------------------------------------------------------------------------------------
def admission_important_dates():
	'''
	sets up important dates regarding admissions
	'''
	filepath=os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,'admission_dates')
	f=file(filepath)
	l=f.readlines()
	f.close()
	now=timezone.now()
	next=now.date().month+1
	if next>12:
		next=1
	next_month=datetime.datetime(now.date().year,next,20,now.time().hour,now.time().minute,now.time().second,now.time().microsecond,now.tzinfo)
	for i in l:
		a=admission.models.dates()
		a.date=timezone.now()
		a.activity=i
		a.valid_upto=next_month
		a.save()
function_list.append(admission_important_dates)
#------------------------------------------------------------------------------------------------
def admission_notices():
	'''
	sets up the notices regarding admissions
	'''
	filepath=os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,'admission_notices')
	files_available=os.listdir(filepath)
	cat=mainsite.models.notification_category.objects.all()[2]
	for i in files_available:
		a=mainsite.models.notification()
		a.title=clean_to_string(i.capitalize())
		a.description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed quis odio vehicula, lobortis ante hendrerit, sodales dolor. Pellentesque quis massa in tellus vulputate pretium vel id ligula. Suspendisse potenti. Donec efficitur est odio, sit amet varius eros ornare in. </p>'
		a.publish_date=timezone.now()
		a.category=cat
		a.save()

		f=file(os.path.join(filepath,i))
		lines=f.readlines()
		f.close()
		new_lines=[clean_to_string(iasd) for iasd in lines]
		for ind,v in enumerate(new_lines):
			s=mainsite.models.Slot()
			s.notif=a
			s.text=v
			s.order=ind
			s.save()
function_list.append(admission_notices)
#------------------------------------------------------------------------------------------------
def admission_categories():
	'''
	sets up the admission categories
	'''
	filepath=os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,'admission_cutoff')
	f=file(os.path.join(filepath,'category'))
	l=f.readlines()
	f.close()
	for i in l:
		a=admission.models.category()
		a.name,a.code=i.split(',')
		a.save()
function_list.append(admission_categories)		
#------------------------------------------------------------------------------------------------
def admission_cutoff_and_courses():
	'''
	sets up the courses and the cutoffs in the college
	'''
	for c in office.models.course.objects.all():
		cs=admission.models.cutoff_subject()
		cs.valid_upto=timezone.now()
		cs.course=c
		cs.save()
		for i in admission.models.category.objects.all():
			a=admission.models.category_cutoff()
			a.category=i
			a.cutoff_subject=cs
			x=random.random()
			a.science=round(random.choice([70,60,80])+(x*19),2)
			x=random.random()
			a.humanities=round(random.choice([70,60,80])+(x*19),2)
			x=random.random()
			a.commerce=round(random.choice([70,60,80])+(x*19),2)
			a.save()
	
function_list.append(admission_cutoff_and_courses)
#------------------------------------------------------------------------------------------------
def admission_candidates():
	'''
	sets up the results in the interviews and such
	'''
	filepath=os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,'admission_candidates')
	files=os.listdir(filepath)
	courses_available=office.models.course.objects.all()
	category_available=admission.models.category.objects.all()
	for i in files:
		ac=college_forms.models.admission_candidate()
		temp_name=i.strip('.jpg').split('_')
		ac.first_name=temp_name[0]
		ac.last_name=temp_name[-1]
		try:
			ac.middle_name=temp_name[1] if temp_name[1]!=temp_name[-1] else ''
		except:
			pass
		f=file(os.path.join(filepath,i))
		ac.picture=File(f)
		ac.email=i+'@gmail.com'
		ac.password='arjoonn'
		ac.stream=random.choice([1,2,3])
		ac.course=random.choice(courses_available)
		ac.category=random.choice(category_available)
		ac.bfs=round((80+(random.random()*20)),2)
		ac.save()
		f.close()
function_list.append(admission_candidates)
		
			
			
#------------------------------------------------------------------------------------------------
def FAQ():
	'''
	sets up the faq for the website
	'''
	filepath=os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,'admission_FAQ')
	q_file=file(os.path.join(filepath,'question'))
	lines=q_file.readlines()
	q_file.close()
	q_a=[]
	temp=[]
	for i,k in enumerate(lines):
		if i%2==0:
			temp.append(k)
		if i%2!=0:
			temp.append(k)
			q_a.append(temp)
			temp=[]
	for k,i in enumerate(q_a):
		a=admission.models.q_a()
		a.question=i[0]
		a.answer=i[1]
		a.rank=k
		a.save()
function_list.append(FAQ)
#------------------------------------------------------------------------------------------------
def run_function(fn):
	'''Runs the function and acts as a wrapper'''
	print fn.func_name.replace('_',' ').capitalize(),
	fn()
	print '--------->Done'
	
def run_setup():
	print '================================================================'
	for i in function_list:
		run_function(i)	
	print 'ADMISSION SETUP COMPLETE'
	print '================================================================'
	
