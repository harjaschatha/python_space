import datetime
from django.utils import timezone
from django.http import Http404
from django.core.mail import send_mail
import office


def get_profile(nick):
	"returns the profile if found along with student or not flag"
	student_flag=True
	try:
		#look for student.Student first as the student body is bigger so lokups are faster
		profile=office.models.student.objects.get(nickname=nick)
	except Exception as e:
		student_flag=False
		print '--------------------'
		print 'Not found in student'
		print '------'
		print e
		print '--------------------'
		try:
			#if not in students look in faculty
			profile=office.models.faculty.objects.get(nickname=nick)
		except Exception as e:
			print '--------------------'
			print 'some error in student'
			print '------'
			print e
			print '--------------------'
			#as person not in faculty or student database raise error
			raise Http404
	return profile,student_flag
	
def contact_notification(email_from,email_to,subject,message):
	'''
	Sends an email to email_to and mentions that email_from has sent it
	'''
	msg='Sir/Madam ,\nThis email is from the college website. A person with email Id\n'+str(email_from)+'\n'
	msg+='has attempted to contact you via the college website. In order to keep your contact details private\n'
	msg+='we have contacted you on their behalf. Below is the message intended for you.\n\nCollege Webteam.'
	msg+='\n\nSUBJECT\n'+str(subject)
	msg+='\n--------------------------\nMESSAGE\n'+str(message)
	msg+='\n--------------------------\nEND of MESSAGE'
	send_mail('St. Stephens Website Contact',msg,'web.dev.ssc@gmail.com',[email_to],fail_silently=False)
	
def admission_registration(email_to):
	'''Confirms the registration for email procedure for a person'''
	#create a message
	msg='''Sir/Madam ,
	The St. Stephen's College, admissions department is pleased to inform you that
	your email has been registered for the admission process.
	All further correspondence shall be through this email address that you have provided
	You shall be notified by email if you have cleared cutoffs when they are released.
	
	Your's Sincerely
	St. Stephen's College
	'''
	send_mail('St. Stephens College',msg,'web.dev.ssc@gmail.com',[email_to],fail_silently=False)
