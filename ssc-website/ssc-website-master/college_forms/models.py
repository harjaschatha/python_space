from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

import office
from admission.models import *




class basic_form_class(models.Model):
	'''The basics any form will have.
	The forms can be saved and later submitted.
	'''
	firstname=models.CharField(max_length=40)
	lastname=models.CharField(max_length=40)
	email=models.EmailField()
	
	submit=models.BooleanField(default=True,editable=False)
	submission_date=models.DateField(default=timezone.now(),editable=False)
	
	document1=models.ImageField(upload_to='forms',help_text='Supporting document 1 scanned copy',blank=True,default=None,null=True)
	document2=models.ImageField(upload_to='forms',help_text='Supporting document 2 scanned copy',blank=True,default=None,null=True)

