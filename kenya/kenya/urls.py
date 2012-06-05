from django.conf.urls import patterns, include, url
from django.conf import settings
import patients.views as views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^detail/(?P<id_number>\d+)/', views.detail),
    url(r'^message/(?P<id_number>\d+)/', views.add_message),
    url(r'^add_call/(?P<id_number>\d+)/', views.add_call),
    url(r'^add/', views.add_client),
    url(r'^edit/(?P<id>\d+)/', views.edit_client),
    url(r'^fragment/list/$', views.list_fragment),
    url(r'^fragment/message/(?P<id>\d+)/', views.message_fragment),
    url(r'^fragment/message_list/(?P<id>\d+)/', views.message_list_frag),
    url(r'^fragment/(?P<id>\d+)/', views.client_fragment),
    url(r'^note/(?P<id>\d+)/', views.add_note),
    url(r'^delete_note/(?P<pk>\d+)/', views.delete_note),
    url(r'^visit/(?P<id>\d+)/', views.add_visit),
    url(r'^delete_visit/(?P<pk>\d+)/', views.delete_visit),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^smssync', views.smssync),
    url(r'^$', views.index),
    url(r'^csv/', views.csv),
    url(r'^clientcsv/(?P<id_number>\d+)/', views.clientcsv),
    url(r'^msgcsv/(?P<id_number>\d+)/', views.message_csv),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
)
urlpatterns += staticfiles_urlpatterns()
