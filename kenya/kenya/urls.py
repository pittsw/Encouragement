from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import patients.views as views
import smssync.urls
import shujaa.urls
import httpsms.urls

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^message/(?P<id_number>\d+)/', views.add_message),
    url(r'^message/prompted/(?P<id_number>\d+)/',views.message_prompted),
    url(r'^add_call/(?P<id_number>\d+)/', views.add_call),
    url(r'^add/', views.add_client),
    url(r'^edit/(?P<id>\d+)/', views.edit_client),
    url(r'^fragment/display_client/$', views.client), #Load Main Client Info and Messages
    url(r'^fragment/message/(?P<id>\d+)/', views.message_fragment), #Center Messages Default
    url(r'^fragment/(?P<id>\d+)/', views.client_fragment), #Right Top client info
    url(r'^note/(?P<id>\d+)/', views.add_note),
    url(r'^delete_note/(?P<pk>\d+)/', views.delete_note),
    url(r'^visit/(?P<id>\d+)/', views.add_visit),
    url(r'^visit_history/',views.visit_history),
    url(r'^test/',views.test),
    url(r'^reports/',views.reports),
    url(r'^delete_visit/(?P<pk>\d+)/', views.delete_visit),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index), #Index
    url(r'^clients$', views.clients), #JSON response of clients
    url(r'^csv/', views.csv),
    url(r'^clientcsv/(?P<id_number>\d+)/', views.clientcsv),
    url(r'^msgcsv/(?P<id_number>\d+)/', views.message_csv),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^pregnacy/(?P<id>\d+)/', views.pregnacy),
    url(r'^smssync/', include(smssync.urls)),
    url(r'^shujaa/', include(shujaa.urls)),
    url(r'^httpsms/', include(httpsms.urls)),
)
urlpatterns += staticfiles_urlpatterns()
