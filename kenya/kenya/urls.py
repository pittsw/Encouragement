from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^kenya/patient/(?P<id_number>\d+)/$', 'kenya.views.client'),
	url(r'^kenya/patient/$', 'kenya.views.list_clients'),
	url(r'^kenya/message/$', 'kenya.views.add_message'),
	url(r'^kenya/demo/$', 'kenya.views.list_clients'),
	url(r'^kenya/add/$', 'kenya.views.add'),
	url(r'^kenya/$', 'kenya.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'kenya.views.index'),
)
