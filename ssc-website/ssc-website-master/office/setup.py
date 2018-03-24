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
import mainsite,attendance,office,events,admission,college_forms


def random_fill(string,length):
	'''Randomly fills a string of length 10 using string'''
	new=''
	for i in xrange(length):
		new+=random.choice(string)
	return new	

def clean_to_string(string):
	'''
	removes non ascii characters
	'''
	allowed='ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'#alphabets and numbers
	allowed+=allowed.lower()#lowercase
	allowed+='''!@#$%^&*()'_+=-.,: '''#Special characters
	allowed+='\n\t'#newline etc
	new_str=''
	for i in string:
		if i in allowed:
			new_str+=i
	return new_str
function_list=[]
SETUP_SUPPORT_FOLDER='setup_support'
#------------------------------------------------------------------------------------------------
def course_type():
	'''sets up the course types'''
	name_list=['Undergraduate','Postgraduate','Vocational','Language']
	for i in name_list:
		a=office.models.course_type()
		a.name=i
		a.save()
		print '		',i
function_list.append(course_type)
#------------------------------------------------------------------------------------------------
def courses():
	'''sets up the courses in undergraduate'''
	filepath=os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,'student_photos','college_studentlist')
	if os.path.exists(os.path.join(filepath,'student_list_clean')):
		f=file(os.path.join(filepath,'student_list_clean'),'r')
		import pickle
		data=pickle.load(f)
		f.close()
		names=data.keys()
		done=[]
		course_names=[]
		for i in names:
			s=i.strip().strip('III').strip('II').strip('I')
			s=s.replace(' ','').lower()
			s=s.replace('year','').replace('-seca','').replace('honours','')
			s=s.replace('-secb','').replace('b.a.','').replace('b.sc.','')
			if s not in done:
				done.append(s)
				name=i.strip().strip('III')
				name=name.strip('II').strip('I').replace('YEAR','')
				name=name.replace('-SEC A','').replace('-SEC B','')
				course_names.append(name)
		names=course_names
		ug_course_type=office.models.course_type.objects.first()
		for i in names:
			a=office.models.course()
			a.name=i
			a.course_type=ug_course_type
			a.save()
			print '		',i
	else:
		import student_scraper as stsc
		stsc.scrape()
		courses()
function_list.append(courses)
#------------------------------------------------------------------------------------------------
def groups():
	'''sets up the groups'''
	groupnames=[
		{'n':'Principal',
		'p':None},
		{'n':'Bursar',
		'p':None},
		{'n':'Dean(Residence)',
		'p':None},
		{'n':'Dean(Academic Affairs)',
		'p':None},
		{'n':'Chaplain',
		'p':None},
		{'n':'Public Information Officer',
		'p':None},
		{'n':'Special Assignments',
		'p':None},
		{'n':'Administration',
		'p':None},
		{'n':'Staff Advisor',
		'p':None},
		{'n':'Faculty',
		'p':None},
		{'n':'Students',
		'p':None}]
	for i in groupnames:
		a=Group()
		a.name=i['n']
		a.save()
function_list.append(groups)
#------------------------------------------------------------------------------------------------
def university_papers():
	'''sets up the papers'''
	filepath=os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,'papers')
	if os.path.exists(os.path.join(filepath,'paper_list_clean')):
		f=file(os.path.join(filepath,'paper_list_clean'),'r')
		import pickle
		data=pickle.load(f)
		f.close()
		for course in data.keys():			
			name=course.strip().strip('III')
			name=name.strip('II').strip('I').replace('YEAR','')
			name=name.replace('-SEC A','').replace('-SEC B','')
			crs=office.models.course.objects.get(name=name)
			for sem in data[course].keys():
				for i in data[course][sem]:
					a=office.models.paper()
					a.code=i
					a.name=i
					a.course=crs
					a.semester=(2*int(sem))-1
					a.save()
					print a.semester,'	',i
	else:
		print 'No paper list found'
function_list.append(university_papers)
#------------------------------------------------------------------------------------------------
def faculty():
	'''
	adds faculty. and departments'''
	
	prof_path=os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,'profile')
	def_pic=file(os.path.join(prof_path,'default.jpg'))
	default_picture=File(def_pic)#default profile picture
	depts=os.listdir(os.path.join(prof_path,'profiles'))#list of departments
	nicks_already_used=[]
	for dept in depts:
		#create department
		department=office.models.deptsoc()
		department.is_society=False
		department.name=dept.strip().replace('_',' ').capitalize()
		nick=clean_to_string(dept.strip().replace('_','').replace(' ','').replace('/','').lower())[:10]
		if nick in nicks_already_used:
			nick = 'phy'
		department.nickname=nick
		nicks_already_used.append(nick)
		department.save()
		#list profiles in the department
		profiles=os.listdir(os.path.join(prof_path,'profiles',dept))
		for prof in profiles:
			#create profiles
			f=file(os.path.join(prof_path,'profiles',dept,prof))
			det=f.readlines()
			f.close()
			user=User()
			user.username=prof.strip().replace(' ','').replace('.','').lower()[:-3]
			user.first_name=clean_to_string(prof.strip()[:-4])#account for the extra dot
			user.set_password('asd')
			user.save()
			#create profile
			profile=office.models.faculty()
			profile.user=user
			x=prof.strip().replace(' ','').replace('.','').lower()[:-3]
			profile.nickname=random_fill(x,10)
			profile.title=''
			profile.picture=default_picture
			profile.dept=department
			profile.qualification=clean_to_string(det[2].strip())
			profile.save()
			print '		',profile.user.first_name
	def_pic.close()
function_list.append(faculty)
#------------------------------------------------------------------------------------------------
def students():
	'''sets up students'''
	filepath=os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,'student_photos','college_studentlist')
	if os.path.exists(os.path.join(filepath,'student_list_clean')):
		f=file(os.path.join(filepath,'student_list_clean'),'r')
		import pickle
		data=pickle.load(f)
		f.close()
		#default picture
		picpath=os.path.join(filepath,'default.jpg')
		f=file(picpath)
		#add students
		for course in data.keys():
			name=course.strip().strip('III')
			name=name.strip('II').strip('I').replace('YEAR','')
			name=name.replace('-SEC A','').replace('-SEC B','')
			crs=office.models.course.objects.get(name=name)
			for sem in data[course].keys():
				for stu in data[course][sem]:
					if 'Student Name' in stu:
						continue
					u=User()
					u.username=str(stu).lower().replace(' ','')
					u.first_name=str(stu.split(' ')[0]).lower()
					u.last_name=str(stu.split(' ')[-1]).lower()
					if u.last_name==u.first_name:
						u.last_name=''
					u.set_password('asd')
					try:
						u.save()	
					except Exception as e:
						print '----------'
						print e
						print '----------'
						print u.username
						uname=random.sample(u.username,len(u.username))
						u.username=''.join(uname)
						print u.username
						u.save()
						print '----------'
					a=office.models.student()
					a.user=u
					a.picture=File(f)
					a.nickname=random_fill(stu.replace(' ',''),10)
					#a.course=office.models.course.objects.first()
					a.course=crs
					a.current_semester=(2*sem)-1
					a.save()
		f.close()#close picture file
	
	else:
		import student_scraper as stsc
		stsc.scrape()
		students()
function_list.append(students)

#------------------------------------------------------------------------------------------------

def societies():
	'''
	adds societies for the college
	'''
	soc_path=os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,'Societies')
	socs=os.listdir(soc_path)
	for i in socs:
		cur_path=os.path.join(soc_path,i)
		accepted="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'"
		accepted+='":,.!@#$%^&*()_+=- '
		accepted+='\n'
		files=os.listdir(cur_path)
		logo_flag=False
		for k in files:
			if ('D' or 'd') in k:
				f_d=file(os.path.join(cur_path,k))
			if 'name' in k:
				f_nick=file(os.path.join(cur_path,k))
			if 'logo' in k:
				f_logo=file(os.path.join(cur_path,k))
				logo_flag=True
		if not logo_flag:
			f_logo=file(os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,'loading.png'))
				
		det=f_d.readlines()
		det_new=[]
		for k in det:
			temp=''
			for j in k:
				if j in accepted:
					temp+=j
			temp+='\n'
			det_new.append(temp)
		det=det_new
		try:
			nicks=f_nick.readlines()[0].strip()
		except :
			nicks=i.strip().replace(' ','')[:10].strip()
		f_d.close()
		f_nick.close()
		#accepted the nicknames and details
		soc=office.models.deptsoc()
		soc.is_society=True
		soc.name=i.strip()
		try:
			soc.logo=File(f_logo)
		except Exception as e:
			print e
			print '---------------------------'
			print 'It appears we have no logo for this society'
		soc.nickname=nicks
		soc.founding_date=timezone.now()
		soc.description=unicode(''.join(det_new))
		soc.save()
		f_logo.close()

function_list.append(societies)
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
	print 'OFFICE SETUP COMPLETE'
	print '================================================================'
	
