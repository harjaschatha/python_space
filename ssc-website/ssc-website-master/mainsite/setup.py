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
function_list=[]
SETUP_SUPPORT_FOLDER='setup_support'




def homepage_slideshow(slideshow_pic_folder='homepage'):
	'''sets up the slideshow files in the homepage'''
	filepath=os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,slideshow_pic_folder)
	files=os.listdir(filepath)
	for i in files:
		f=File(file(os.path.join(filepath,i)))
		a=mainsite.models.home_slideshow_photo()
		a.associated_photo=f
		a.name=i
		a.save()
function_list.append(homepage_slideshow)
#------------------------------------------------------------------------------------------------
def notification_categories():
	'''Setup the notification categories'''
	categories=['Notices',"Principal's Desk","Admission Notices"]
	for c in categories:
		cat=mainsite.models.notification_category()
		cat.name=c
		cat.save()
		print c
function_list.append(notification_categories)
#------------------------------------------------------------------------------------------------
def principal_desk_notices(principal_desk_folder='principal_desk'):
	'''sets up the principal desk notices'''
	filepath=os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,principal_desk_folder)
	files_all=os.listdir(filepath)
	files=[i for i in files_all if '~' not in i]
	cat=mainsite.models.notification_category.objects.all()[1]
	for i in files:
		f=file(os.path.join(filepath,i))
		a=mainsite.models.notification()
		a.title=clean_to_string(i.split('.')[0].replace('_',' '))
		a.category=cat
		a.associated_file=File(f)
		a.description=clean_to_string(i.replace('_',' '))
		a.save()
		lines=f.readlines()
		f.close()
		new_lines=[clean_to_string(iasd) for iasd in lines]
		text='\n'.join(new_lines)
		s=mainsite.models.Slot()
		s.notif=a
		s.text=text
		s.order=0
		s.save()
		
function_list.append(principal_desk_notices)
#------------------------------------------------------------------------------------------------
def notifications(folder='notifications'):
	'''sets up the notifications for the website'''
	filepath=os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,folder)
	folders=os.listdir(filepath)
	cat=mainsite.models.notification_category.objects.first()
	for folder in folders:
		slots=os.listdir(os.path.join(filepath,folder))
		slots.sort()
		a=mainsite.models.notification()
		a.title=folder.split('.')[0].replace('_',' ').capitalize()
		a.description='A notice from the college.'
		a.category=cat
		a.save()
		for sno in slots:
			files=os.listdir(os.path.join(filepath,folder,sno))
			s=mainsite.models.Slot()
			s.notif=a
			s.order=sno
			if 't' in files:
				f=file(os.path.join(filepath,folder,sno,'t'))
				lines=f.readlines()
				new_lines=[clean_to_string(iasd) for iasd in lines]
				text='\n'.join(new_lines)
				s.text=text
				f.close()
			if 'l' in files:
				fl=file(os.path.join(filepath,folder,sno,'l'))
				s.link=fl.readline()
				fl.close()
			if 'f' in files:
				f_file=file(os.path.join(filepath,folder,sno,'f'))
				s.associted_file=File(f_file)
			if 'i' in files:
				f_pic=file(os.path.join(filepath,folder,sno,'i'))
				s.picture=File(f_pic)
			s.save()
			try:
				f_file.close()
			except: 
				pass
			try:
				f_pic.close()
			except:
				pass
function_list.append(notifications)
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
	print 'MAINSITE SETUP COMPLETE'
	print '================================================================'
	
