from django.contrib import admin

from admission.models import *

def admit_students(modeladmin,request,queryset):
	'''
	sets the admitted flag on students to true
	'''
	queryset.update(admitted=True)
admit_students.short_description='Admit selected students to college'


class dates_admin(admin.ModelAdmin):
	list_display=['activity','date','valid_upto']
	list_filter=['date','valid_upto']
	search_fields=['activity']
	
class category_cutoff_inline(admin.TabularInline):
	'''
	inline model for category cutoff
	'''
	model=category_cutoff
class cutoff_subject_admin(admin.ModelAdmin):
	'''
	admin for cutoffs
	'''
	inlines=[category_cutoff_inline]
class admission_candidate_admin(admin.ModelAdmin):
	'''
	admin for admission_candidate
	'''
	exclude=['cutoff_status']
	list_display=['thumbnail','email','stream','course','category','clear_cutoff','admitted']
	list_filter=['stream','course','category']
	search_fields=['first_name','middle_name','last_name','email']
	actions=[admit_students]
	
admin.site.register(admission_candidate,admission_candidate_admin)	
admin.site.register(cutoff_subject,cutoff_subject_admin)
admin.site.register(dates,dates_admin)
