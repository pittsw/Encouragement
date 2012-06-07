from django.conf.urls.defaults import *

import smssync.views as views

urlpatterns = patterns('',
    url(r'^$', views.smssync),
)
