from django.conf.urls import patterns, include, url
from django.conf import settings
import patients.views as views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^patient/(?P<id_number>\d+)/', views.client),
    url(r'^detail/(?P<id_number>\d+)/', views.detail),
    url(r'^message/(?P<id_number>\d+)/', views.add_message),
    url(r'^message/', views.add_message),
    url(r'^demo/', views.list_clients),
    url(r'^add/', views.add_client),
    url(r'^edit/(?P<id>\d+)/', views.edit_client),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^overview/', views.over),
    url(r'^smssync', views.smssync),
    url(r'^$', views.over),
)
urlpatterns += staticfiles_urlpatterns()
