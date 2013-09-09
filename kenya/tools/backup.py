#set up Django
import os,sys,datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from django.core.management import setup_environ
from kenya import settings

setup_environ(settings)
#end Django setup

#Django Imports
from django.core import serializers, management

#App Imports
import backend.models as backend
import patients.tasks as tasks
import patients.models as patients

#Python Imports
from StringIO import StringIO
import json, datetime

# backup all of patients
fp = open(str(datetime.date.today())+"_bk.json","w")
management.	call_command("dumpdata","patients",indent=2,stdout=fp)
fp.close()

# backup all of Shujaa Messages

# backup all of Transports
