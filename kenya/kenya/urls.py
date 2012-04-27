from django.conf.urls import patterns, include, url

import patients.views as views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^kenya/patient/(?P<id_number>\d+)/', views.client),
	url(r'^kenya/patient/', views.list_clients),
	url(r'^kenya/message/', views.add_message),
	url(r'^kenya/demo/', views.list_clients),
	url(r'^kenya/add/', views.add_client),
	url(r'^kenya/$', views.index),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^kenya/detail/(?P<id_number>\d+)/', views.detail),
	url(r'^kenya/message/(?P<id_number>\d+)/', views.add_message),
	url(r'^kenya/overview', views.over),
    url(r'^kenya/smssync', views.smssync),
    url(r'^$', views.over),
)
