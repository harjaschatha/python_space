import office
import random
from django.db import models
from django.utils import timezone
from django.forms import ModelForm

class attendance_control(models.Model):
	'''Control variables and actions for attendance application'''
	cutoff=models.FloatField(default=2.0/3)
	
class paper_attendance(models.Model):
	'''Class to record common characteristics for a paper's attendance records.
	It is common for all student studying the paper.
	Date_from=starting attendance date
	Date_to=ending attendance date
	paper=paper for which attendance will be recorded
	
	The lecture,tutorial,practical totals for this paper
	'''
	def __unicode__(self):
		return self.paper.__unicode__()
	date_from=models.DateField('Date of counting first attendance.',default=timezone.now())
	date_to=models.DateField('Date of counting last attendance.',default=timezone.now())
	paper=models.ForeignKey(office.models.paper,related_name='paper')
	
	taught_by=models.ForeignKey(office.models.faculty,related_name='taught_by',default=None,blank=True,null=True)
	
	lecture=models.PositiveSmallIntegerField('Total Lecture',default=0)
	tutorial=models.PositiveSmallIntegerField('Total Tutorial',default=0)
	practical=models.PositiveSmallIntegerField('Total Practical',default=0)
		
class student_attendance(models.Model):
	'''Class to record a student's attendance in a paper.
	Student attendance in a paper.
	Relates to a class attendance which holds the total attendance.
	The classes attended and the adjustments for the classes.
	'''
	def __unicode__(self):
		return self.student.__unicode__()+'-'+self.class_attendance.paper.__unicode__()
	student=models.ForeignKey(office.models.student,related_name='student')
	class_attendance=models.ForeignKey(paper_attendance,related_name='class_attendance')
	
	lecture=models.PositiveSmallIntegerField('Lecture Attended',default=0)
	tutorial=models.PositiveSmallIntegerField('Tutorial Attended',default=0)
	practical=models.PositiveSmallIntegerField('Practical Attended',default=0)
	
	a_lecture=models.PositiveSmallIntegerField('Lecture Adjustment(ECA etc)',default=0)
	a_tutorial=models.PositiveSmallIntegerField('Tutorial Adjustment(ECA etc)',default=0)
	a_practical=models.PositiveSmallIntegerField('Practical Adjustment(ECA etc)',default=0)
class eca_request(models.Model):
	'''Class to store an ECA request.
	Signed is filled by the staff advisor or hod.
	Approved is filled by principal.
	Null means not seen.'''
	stud=models.ForeignKey(office.models.student,related_name='stud')
	signed=models.NullBooleanField(default=None)#signed by HOD/staff advisor
	approved=models.NullBooleanField(default=None)#signed by principal
	description=models.TextField(help_text='Nature of activity requiring absence from class.')
	soc=models.ForeignKey(office.models.deptsoc,related_name='society',help_text='Department/Society under which activity was done.')
	last_modified=models.DateTimeField(auto_now=True)#when last modified
	created=models.DateTimeField(auto_now_add=True)#when created
	
	def save(self,*args,**kwargs):
		try:
			old=eca_request.objects.get(pk=self.id)
		except Exception as e:
			print e
		else:
			lg=eca_log()
			lg.req=old
			#get old data and new data
			olddata=""
			newdata=""
			if old.stud!=self.stud:#student has changed
				olddata+='Stud:'+old.stud.__unicode__()+'\n'
				newdata+='Stud:'+self.stud.__unicode__()+'\n'
			if old.signed!=self.signed:#if sign has changed
				olddata+='Signed:'+str(old.signed)+'\n'
				newdata+='Signed:'+str(self.signed)+'\n'
			if old.approved!=self.approved:#if approval has changed
				olddata+='Signed:'+str(old.approved)+'\n'
				newdata+='Signed:'+str(self.approved)+'\n'
			if old.description!=self.description:#if description has changed
				olddata+='Signed:'+str(old.description)+'\n'
				newdata+='Signed:'+str(self.description)+'\n'
			if old.soc!=self.soc:#if society has changed
				olddata+='Signed:'+str(old.soc.__unicode__())+'\n'
				newdata+='Signed:'+str(self.soc.__unicode__())+'\n'			
			#save the log
			lg.save()
		#save the data to database
		super(eca_request,self).save(*args,**kwargs)
		
class eca_date(models.Model):
	'''Class to store ECA date'''
	related_eca_request=models.ForeignKey(eca_request)
	start=models.DateTimeField()
	end=models.DateTimeField()

class eca_log(models.Model):
	'''A class to keep track of the activities in the ECA models.
	Tracks activities after creation'''
	def __unicode__(self):
		return 'req='+str(self.req.id)+','+str(self.id)
	stamp=models.DateTimeField(auto_now_add=True)#timedate stamp of the activity
	req=models.ForeignKey(eca_request,related_name='req')#The eca_request under consideration
	old_data=models.TextField(blank=True)#old data
	new_data=models.TextField(blank=True)#new data
	

#--------------------------FORMS------------------------------
class eca_request_form(ModelForm):
	class Meta:
		model=eca_request
		exclude=['approved','stud']
class eca_date_form(ModelForm):
	class Meta:
		model=eca_date
		fields=['start','end']
class eca_sign_form(ModelForm):
	class Meta:
		model=eca_request
		exclude=['approved']
class paper_attd_form(ModelForm):
	class Meta:
		model=paper_attendance
		exclude=['paper','taught_by']
class stu_attd_form(ModelForm):
	class Meta:
		model=student_attendance
		exclude=['class_attendance','student']
#-------------------------------------------------------------
