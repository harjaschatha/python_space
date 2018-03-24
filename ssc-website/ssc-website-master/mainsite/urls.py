from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()
from mainsite import views,feeds

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stephens.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^$',views.home,name='site_home'),
    url(r'^notification_rss',feeds.Notifications_feed(),name='notification_feed'),
    url(r'^principal_rss',feeds.Principal_feed(),name='principal_feed'),
    url(r'^admission_rss',feeds.Admission_feed(),name='admission_notice_feed'),
    
    url(r'^academics/$',views.academics,name='academics_home'),
    url(r'^course/(?P<cid>\d+)/$',views.course_detail,name='course_detail'),

    url(r'^society/$',views.society,name='society_home'),
    url(r'^society/(?P<nick>\S+)/$',views.society_detail,name='society_detail'),

    url(r'^department/$',views.department,name='department_home'),
    url(r'^department/(?P<nick>\S+)/$',views.department_detail,name='department_detail'),

    url(r'^alumni/$',views.alumni,name='alumni_home'), 
    url(r'^archive/$',views.archive,name='archive_home'),
    url(r'^contact/$',views.contact,name='contact_home'),
    
    url(r'^notice/$',views.notice_home,name='notice_home'),
    url(r'^principal/$',views.principal_home,name='principal_home'),
    url(r'^notice/(?P<cid>\d+)/$',views.notice_detail,name='notice_detail'),
    
    url(r'^profile/$',views.profile_detail,name='profile_detail_general'),
    url(r'^profile/(?P<nick>\S+)/$',views.profile_detail,name='profile_detail'),
    url(r'^profile/(?P<nick>\S+)/upload/$',views.profile_upload,name='profile_material_upload'),
    url(r'^profile/(?P<nick>\S+)/contact/$',views.profile_contact,name='profile_contact'), 
)
