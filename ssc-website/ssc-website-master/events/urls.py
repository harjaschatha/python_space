from django.conf.urls import patterns, include, url

from events import views

urlpatterns = patterns('',
	url(r'^$',views.home,name='event_home'),
	url(r'^(?P<year>\d+)/(?P<month>\d+)/$',views.event_month,name='event_month'),
	url(r'^(?P<nick>\S+)/$',views.event_detail,name='event_detail'),
    
)
