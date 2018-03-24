from django.conf.urls import patterns, include, url
from college_forms import views

urlpatterns = patterns(
	'',
	url('^$',views.home,name='forms_home'),
	
	)
