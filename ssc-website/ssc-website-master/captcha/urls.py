from django.conf.urls import patterns, include, url

import .views as views

urlpatterns = patterns(
	'',
	url(r'^get/$',views.get_captcha,name='get_captcha'),
	url(r'^check/$',views.check_captcha,name='check_captcha')
)
