#set up Django
import os,sys,datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from django.core.management import setup_environ
from kenya import settings

setup_environ(settings)

import backend.models as backend
import patients.tasks as tasks
import patients.models as patients


clients = tasks.get_clients_to_message(day=False,hour=False)
clients = clients.exclude(id__in=(6,9,12,1))
messages = {}
for c in clients:
	messages[c] = tasks.get_message(c)
	

for c,ms in messages.iteritems():
	print c
	for i,m in enumerate(ms):
		print i,m
		tasks.message_client(c,None,"System",m)


