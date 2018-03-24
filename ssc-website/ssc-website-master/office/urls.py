from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from mainsite import views

urlpatterns = patterns('',
	url(r'^$',views.home,name='site_home'),
)
