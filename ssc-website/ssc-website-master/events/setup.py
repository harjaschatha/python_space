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
function_list=[]
SETUP_SUPPORT_FOLDER='setup_support'

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



def locations():
	'''
	locations in college'''
	filepath=os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,'locations')
	f=file(filepath)
	loc=f.readlines()
	f.close()
	for i in loc:
		l=events.models.Location()
		l.name=i.strip().capitalize()[:40]
		l.save()
function_list.append(locations)
#------------------------------------------------------------------------------------------------
def events_in_college():
	ev_path=os.path.join(os.getcwd(),SETUP_SUPPORT_FOLDER,'events')
	
function_list.append(events_in_college)
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
	print 'EVENTS SETUP COMPLETE'
	print '================================================================'
	
