#!/usr/bin/python

#------- Setup Django Framework --------#
import os,sys,datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from django.core.management import setup_environ
from kenya import settings

setup_environ(settings)

from  django.db.models import Q

import backend.models as backend
import patients.tasks as tasks
import patients.models as patients

#--------- End Django Framework ---------#

not_sent = patients.Message.objects.filter(Q(id__gt=87) & Q(id__lt=128)).exclude(sent_by="Client")\
.exclude(id__in=[88,96,97,98,103,104,116])
	
for m in not_sent:
	#tasks.message_client(m.client_id,None,"System",m.content)
	#m.client_id.last_msg_system = datetime.date.today()
	#m.client_id.save()
	print m.content
