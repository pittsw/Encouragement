#!/usr/bin/python

#set up command line option parser
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p","--permanent",action="store_true",help="flag to use permanent databases",default=False)

(options,args) = parser.parse_args()


#set up django framework
import sys,os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from django.core.management import setup_environ
from kenya import settings

#use temp database
if(options.permanent==False):
	
	settings.DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': '../temp.db'
		},
	}

setup_environ(settings)

from django.core import serializers, management

#if using temp database sync
if(options.permanent==False):
	management.call_command('syncdb',interactive=False)

#import models 
import backend.models as backend
import patients.tasks as tasks
import patients.models as patients
