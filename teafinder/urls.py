from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'teafinder.views.home', name='home'),
    # url(r'^teafinder/', include('teafinder.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'teafinder$', 'tea.views.index'),
    url(r'teafinder/get_teas', 'tea.views.get_teas'),
    url(r'teafinder/get_tea', 'tea.views.get_tea'),
)

urlpatterns += staticfiles_urlpatterns()
