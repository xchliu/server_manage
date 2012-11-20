from django.conf.urls import patterns, include, url
from server_list.views import home,server_add
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',home),
    url(r'^add/',server_add),
    # Examples:
    # url(r'^$', 'server_manage.views.home', name='home'),
    # url(r'^server_manage/', include('server_manage.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
