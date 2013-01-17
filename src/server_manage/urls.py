from django.conf.urls import patterns, include, url
from server_list.views import home,server_add,add_project
from report.views import report_web
from meta_data.views import server_detail
from meta_data.views import project_detail,ip_detail
# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',home),
    url(r'^add/',server_add),
    url(r'^report/',report_web),
    url(r'^add_pro/',add_project),
    url(r'^server_detail/',server_detail),
    url(r'^project_detail/',project_detail),
    url(r'^ip_detail/',ip_detail),
    # Examples:
    # url(r'^$', 'server_manage.views.home', name='home'),
    # url(r'^server_manage/', include('server_manage.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
