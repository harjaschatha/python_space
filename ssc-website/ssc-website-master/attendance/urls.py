from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from attendance import views

urlpatterns = patterns(
	'',
	url(r'^$',views.home,name='attendance_home'),
	url(r'^(?P<studentid>\d+)/$',views.student_id,name='student_id'),
	url(r'^short/$',views.short_attendance,name='short_attendance'),
	url(r'^eca/$',views.ECA_home,name='home_eca'),
	url(r'^eca/list/$',views.ECA_list,name='view_eca'),
	url(r'^eca/new/$',views.ECA_new,name='request_eca'),
	url(r'^eca/sign/$',views.ECA_sign,name='sign_eca'),
	url(r'^eca/approve/$',views.ECA_approve,name='approve_eca'),
	url(r'^class/(?P<paper_id>\d+)$',views.class_attendance,name='class_attendance'),
	url(r'^classupdate/(?P<paper_id>\d+)$',views.class_attend_upd,name='class_attendance_update'),
)
