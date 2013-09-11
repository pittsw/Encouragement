#!/usr/bin/python

#------- Setup up Option Parser ------#
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p","--permanent",action="store_true",help="flag to use permanent databases",default=False)
parser.add_option("-l","--log",help="logging level",default="WARNING")

(options,args) = parser.parse_args()
#------- End Option Parser ------#

#--------- Setup Logging --------#
import logging, logging.config

log_config = {
	'version':1,
	'disable_existing_loggers':False,
	'formatters':{
		'standard':{
			'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
		}
	},
	'handlers': {
		'default': {
			'level':options.log,    
			'class':'logging.StreamHandler',
		},  
		},
	'loggers': {
		'test': {                  
			'handlers': ['default'],        
			'level': 'INFO',  
			'propagate': True  
		}
	}
}

logging.config.dictConfig(log_config)

logger = logging.getLogger('test')

#-------- End Logging ------#

#------- Setup Django Framework --------#
import sys,os,StringIO
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from django.core.management import setup_environ
from kenya import settings

DB_PATH = os.path.dirname(__file__)+'/../temp.db'
#use temp database
if(options.permanent==False):
	settings.DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.sqlite3',
			'NAME': DB_PATH
		},
	}

setup_environ(settings)

from django.core import management

#if using temp database delete old db and sync
if(options.permanent==False):
	logger.warning("Creating Temporary Database")
	
	tmp_stdout = sys.stdout
	if(options.log.upper()!="DEBUG"):
		sys.stdout = open(os.devnull,'w')
	if os.path.isfile(DB_PATH):
		os.remove(DB_PATH)
	management.call_command('syncdb',interactive=False)
	management.call_command('migrate',interactive=False)
	sys.stdout = tmp_stdout

#------- End Django Framework -------#


#import models 
import backend.models as backend
import patients.tasks as tasks
import patients.models as patients

def begin(s):
	print "{0}  {1}  {0}".format("-"*10,s)
	
def end(old=False,new=False):
	if old==new:
		print "PASS"
	else:
		print "FAIL"
	print "\n\n"


# Test: send message
if True:
	begin("Send Message")
	client = patients.Client.objects.get(pk=1)
	old = client.interaction_set.count()
	tasks.message_client(client,None,"System","Test Message")
	new = client.interaction_set.count()
	print "Message Count: Old {} New {}".format(old,new)
	end(old,new-1)
