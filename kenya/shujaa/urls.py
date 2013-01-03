from django.conf.urls.defaults import *

import shujaa.views as views

urlpatterns = patterns('',
    url(r'^$', views.smssync),
    url(r'^p$', views.print_request),
)
