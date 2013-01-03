from django.conf.urls.defaults import *

import httpsms.views as views

urlpatterns = patterns('',
    url(r'^$', views.httpSMS),
    url(r'^send$', views.sendSMS),
    url(r'^system$', views.sendSystem),
)
