from django.conf.urls import patterns, include, url

from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
	'',
	url(r'^',include('mainsite.urls')),
	url(r'^login/$','django.contrib.auth.views.login',{'template_name':'login.html'},name='site_login'),
	url(r'^logout/$','django.contrib.auth.views.logout',{'template_name':'logged_out.html'},name='site_logout'),
	url(r'^logout/$','django.contrib.auth.views.logout',{'template_name':'logged_out.html'},name='password_change_done'),
	url(r'^change/$','django.contrib.auth.views.password_change',{'template_name':'pwd_reset.html'},name='password_change'),
	url(r'^office/',include('office.urls')),
	url(r'^attendance/',include('attendance.urls')),
	url(r'^event/',include('events.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^admissions/',include('admission.urls')),
	url(r'^forms/',include('college_forms.urls')),
	#url(r'^site/',include('django.contrib.flatpages.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

