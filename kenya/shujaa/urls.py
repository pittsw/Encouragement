from django.conf.urls.defaults import *

import shujaa.views as views

urlpatterns = patterns('',
    url(r'^$', views.receive),
    url(r'^p$', views.print_request),
    url(r'^testmessage/$',views.testmessage)
)
