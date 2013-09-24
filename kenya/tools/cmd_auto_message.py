#------- Setup up Option Parser ------#
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s","--send",action="store_true",help="flag to send messages",default=False)
parser.add_option("-d","--day",action="store_false",help="flag to send messages for today only",default=True)
parser.add_option("-H","--hour",action="store_false",help="flag to send messages for this hour only",default=True)
(options,args) = parser.parse_args()
#------- End Option Parser ------#

#------- Setup Django Framework --------#
import os,sys,datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from django.core.management import setup_environ
from kenya import settings

setup_environ(settings)

import backend.models as backend
import patients.tasks as tasks
import patients.models as patients
#--------- End Django Framework ---------#

print "Day: (%s) Hour: (%s) Send: (%s)"%(options.day,options.hour,options.send)

#get clients 
sent = tasks.send_automated_message(day=options.day,hour=options.hour,send=options.send)

up_comming = tasks.send_up_coming(hour=options.hour)


