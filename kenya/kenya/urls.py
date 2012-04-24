from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^kenya/patient/(?P<id_number>\d+)/$', 'patients.views.client'),
	url(r'^kenya/patient/$', 'patients.views.list_clients'),
	url(r'^kenya/message/$', 'patients.views.add_message'),
	url(r'^kenya/demo/$', 'patients.views.list_clients'),
	url(r'^kenya/add/$', 'patients.views.add_client'),
	url(r'^kenya/$', 'patients.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'patients.views.index'),
)
