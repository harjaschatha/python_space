from django.db import models
from django.core.urlresolvers import reverse
from django import forms
from django.utils import timezone
import office
def get_hash(string):
		'''returns the hash of a string.
		length=56, sha224 implementation'''
		import hashlib
		return hashlib.sha224(string).hexdigest()
class admission_control(models.Model):
	'''
	models to control the admission application.
	General controls
	'''
	accept_admission_forms=models.BooleanField(default=False)
	prospectus=models.FileField(upload_to='admission')
	
class dates(models.Model):
	'''
	The important dates related to admissions.
	Published on the website.
	valid_upto shows that this notification is valid upto which date.
	'''
	def __unicode__(self):
		return str(self.activity)
	date=models.DateField()
	activity=models.CharField(max_length=100)
	valid_upto=models.DateField()

class category(models.Model):
	'''
	stores the various quotas for admission.
	New quotas may be added.
	'''
	def __unicode__(self):
		return str(self.code)
	name=models.CharField(max_length=50)
	code=models.CharField(max_length=5)
	
class cutoff_subject(models.Model):
	'''
	cutoffs for a course.
	Relation model. Holds cutoffs for different categoris and governs their validity.
	'''
	def __unicode__(self):
		return str(self.course.__unicode__())
	valid_upto=models.DateField()
	course=models.ForeignKey(office.models.course,related_name='course_for')
	
	
class category_cutoff(models.Model):
	'''
	stores cutoffs for a category.
	Cutoffs for a category in the admission reservation procedure.
	'''
	category=models.ForeignKey(category,related_name='category')
	science=models.FloatField()
	commerce=models.FloatField(null=True,blank=True,default=None)
	humanities=models.FloatField(null=True,blank=True,default=None)
	cutoff_subject=models.ForeignKey(cutoff_subject,related_name='cutoff_subject')
class q_a(models.Model):
	'''
	question answer model.
	contains the question text along with answer text and a rank value.
	Rank is where the question is displayed
	'''
	question=models.TextField()
	answer=models.TextField()
	rank=models.SmallIntegerField()

class admission_candidate(models.Model):
	'''
	model to represent an admission candidate
	-----------------------------------------
	Things to be supplied by candidate
	1. name
	2. valid email id
	3. photograph
	4. marksheets
	5. payment challans
	'''
	def __unicode__(self):
		return str(self.firstname)+' '+str(self.lastname)
	def get_absolute_url(self):
		return reverse('admission_candidate_detail',args=[self.id])
	def set_password(self,string):
		'''
		sets the password value  to the hash of the given string
		'''
		self.password=get_hash(string)
	def check_password(self,string):
		'''
		checks if string is same as the password by comparing hashes
		'''
		current=self.password
		entered=get_hash(string)
		if current==entered:
			return True
		return False
	def clear_cutoff(self):
		'''
		checks if candidate clears cutoff
		Returns True if candidate clears cutoff for his/her category 
		Returns False if category cutoff is not cleared. OR if cutoffs are not yet defined
		'''
		old_value=self.cutoff_status
		new_value=old_value
		if len(category_cutoff.objects.all())==0:
			new_value=False#ie no cutoffs have been declared
			
		cutoff=category_cutoff.objects.filter(cutoff_subject__course=self.course).filter(category=self.category).filter(cutoff_subject__valid_upto__lte=timezone.now())[0]
		
		if self.stream==1:#from science
			if self.bfs>=cutoff.science:
				new_value=True
			else:
				new_value=False
		if self.stream==2:#from commerce
			if self.bfs>=cutoff.commerce:
				new_value=True
			else:
				new_value=False
		if self.stream==3:#from humanities
			if self.bfs>=cutoff.humanities:
				new_value=True
			else:
				new_value=False
		if new_value==old_value:
			return new_value
		else:
			self.cutoff_status=new_value
			self.save()
			return new_value
	def thumbnail(self):
	        if self.picture:
      	        	addr=self.picture.url
	        	addr.strip('/')
	        	
	                return u'<img src="'+addr+'" width=60 height=60 />'

	        else:
	        	return u'No image file found'
	thumbnail.short_description ='Thumbnail'
	thumbnail.allow_tags=True
		
	clear_cutoff.boolean=True
	clear_cutoff.short_description='Has cleared course cutoff?'
	clear_cutoff.admin_order_field='cutoff_status'
	
	firstname=models.CharField(max_length=40)
	middlename=models.CharField(max_length=40,blank=True)
	lastname=models.CharField(max_length=40,blank=True)
	email=models.EmailField()
	
	submit=models.BooleanField(default=True,editable=False)
	submission_date=models.DateField(auto_now_add=True)
	
	document_1=models.ImageField(upload_to='admissions/documents/%Y/%m/%d',help_text='Supporting document 1 scanned copy',blank=True,default=None,null=True)
	document_2=models.ImageField(upload_to='admissions/documents/%Y/%m/%d',help_text='Supporting document 2 scanned copy',blank=True,default=None,null=True)
	document_3=models.FileField(upload_to='admissions/documents/%Y/%m/%d',null=True,blank=True,default=None,help_text='Scanned copy of supporting document 3(optional)')
	document_4=models.FileField(upload_to='admissions/documents/%Y/%m/%d',null=True,blank=True,default=None,help_text='Scanned copy of supporting document 4(optional)')
	
	#candidate personal information
	
	picture=models.ImageField(upload_to='admissions/photos/%Y/%m/%d',help_text='Photograph of candidate taken in last 6 months',blank=True)
	
	#admission indormation
	STREAM_CHOICES=[
			(1,'Sciences'),
			(2,'Commerce'),
			(3,'Humanities')
			]
			
	stream=models.SmallIntegerField('Stream applicable to you',choices=STREAM_CHOICES,default=1)
	course=models.ForeignKey(office.models.course,related_name='course_applied',help_text='Course you want to apply for')
	category=models.ForeignKey(category,related_name='category_applied',help_text='Category applicable to you')
	bfs=models.FloatField("Best Four Subject's Marks")
	
	cutoff_status=models.BooleanField(default=False)#status of cutoff clearence
	admitted=models.BooleanField(default=False)#status of admission



class admission_form(forms.ModelForm):
	class Meta:
		model=admission_candidate
		exclude=['cutoff_status','admitted']
