from django.conf.urls import patterns, include, url

from admission import views

urlpatterns = patterns('',
	url(r'^$',views.home,name='admission_home'),
	url(r'^procedure/$',views.procedure,name='admission_procedure'),
	url(r'^dates/$',views.dates,name='admission_dates'),
	url(r'^notices/$',views.notice,name='admission_notices'),
	url(r'^cutoff/$',views.cutoff,name='admission_cutoff'),
	url(r'^result/$',views.result,name='admission_result'),
	url(r'^form/$',views.admission_form,name='admission_form'),
	url(r'^faq/$',views.faq,name='admission_faq'),
	
	url(r'(?P<cid>\d+)/$',views.candidate_detail,name='admission_candidate_detail'),
	url(r'^resend/(?P<cid>\d+)$',views.resend_confirmation,name='resend_admission_email'),
)
