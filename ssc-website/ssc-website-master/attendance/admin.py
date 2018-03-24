from django.contrib import admin
from attendance.models import *


#---------------------Filters-----------------
#--------------------Admins-------------------

class student_attendance_inline(admin.TabularInline):
	'''Inline addition for student_attendance'''
	model=student_attendance
	extra=20
	
class paper_attendance_admin(admin.ModelAdmin):
	'''Paper attendance admin'''
	
	inlines=[student_attendance_inline]
	
	list_display=['paper','date_from','date_to']
	list_filter=['date_from','date_to']
	search_fields=['paper']
	
class student_attendance_admin(admin.ModelAdmin):
	'''admin for student attendance'''
	list_filter=['class_attendance']
	search_fields=['student__user']

class eca_date_inline(admin.TabularInline):
	'''Inline addition of dates of absence'''
	model=eca_date
	extra=1
class eca_request_admin(admin.ModelAdmin):
	'''Admin for eca_request'''
	inlines=[eca_date_inline]
	
	list_display=['stud','approved','soc']
	list_filter=['approved','soc']
	search_fields=['stud__user__first_name','description']
class eca_log_admin(admin.ModelAdmin):
	list_display=('req','stamp')
	list_filter=('req','stamp')
	
admin.site.register(student_attendance,student_attendance_admin)
admin.site.register(paper_attendance,paper_attendance_admin)
admin.site.register(eca_request,eca_request_admin)
admin.site.register(eca_log,eca_log_admin)
