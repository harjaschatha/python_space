import os
import sys
import shutil
import random
import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stephens.settings")

from django.core.files import File


from django.contrib.auth.models import User,Group
from django.core.management import execute_from_command_line
from django.utils import timezone
from django.conf import settings

#cleanup of the existing files etc
try:
	os.remove(os.path.join(os.getcwd(),'db.sqlite3'))
except Exception as e:
	print '================================================================'
	print 'Looks like you have already removed the database.'	
	print 'here is the traceback just for completeness'
	print '================================================================'
	print e
	print '================================================================'
	print 'Moving on'
else:
	print 'Removed the existing database'
	print '================================================================'
	print 'Moving on'
	
try:
	print 'Cleaning media root'
	path=settings.MEDIA_ROOT
	shutil.rmtree(path)
except Exception as e:
	print e
else:
	print 'Done'
print '================================================================'
#cleanup complete
#create the database tables
print 'Collecting static'
execute_from_command_line(['manage.py','collectstatic','--noinput'])
print 'Done'
print '================================================================'
print 'Syncdb'
execute_from_command_line(['manage.py','syncdb','--noinput'])
print 'Creating superuser'
sup=User()
sup.is_staff=True
sup.is_superuser=True
sup.set_password('asd')
sup.username='ghost'
sup.save()
print '================================================================'
#------------------------------------------------------------------------------------------------
#----------------------------------Now the setup of data starts------------------------------------------
#------------------------------------------------------------------------------------------------
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
print '================================================================'
print 'SETTING UP THE WEBSITE'
print '================================================================'
from mainsite import setup as mainsite_setup
from attendance import setup as attendance_setup
from office import setup as office_setup
from events import setup as events_setup
from admission import setup as admission_setup
from college_forms import setup as college_forms_setup
setup_list=[office_setup,
		mainsite_setup,
		attendance_setup,
		admission_setup,
		events_setup,
		college_forms_setup
		]
#------------------------------------------------------------------------------------------------
if __name__=='__main__':
	for i in setup_list:
		i.run_setup()
	print '================================================================'
	print 'SETUP COMPLETE'
	print '================================================================'
