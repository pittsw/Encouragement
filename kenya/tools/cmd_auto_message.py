#------- Setup up Option Parser ------#
from optparse import OptionParser
import datetime

def parse_date(option,opt_str,value,parser):
	year,month,day,hour = value
	
	hour = 8 if hour <= 9 else 13 if hour<= 14 else 19
	
	parser.values.time = datetime.datetime(year,month,day,hour)

parser = OptionParser()
parser.add_option("-s","--send",action="store_true",help="flag to send messages",default=False)
parser.add_option("-e","--email",action="store_true",help="flag to send email",default=False)
parser.add_option("-d","--day",action="store_false",help="flag to send messages for all days",default=True)
parser.add_option("-H","--hour",action="store_false",help="flag to send messages for all hours",default=True)
parser.add_option("-a","--auto",action="store_true",help="flag to send automated messages",default=False)
parser.add_option("-v","--visits",action="store_true",help="flag to send visit reminders",default=False)
parser.add_option("-r","--resend",action="store_true",help="flag to resend automated messages",default=False)
parser.add_option("--all",action="store_true",help="flag to send all",default=False)
parser.add_option("--time",action="callback",callback=parse_date,nargs=4,help="change the time to send YYYY MM DD HH",type="int",default=datetime.datetime.today())
(options,args) = parser.parse_args()
print options.time
#------- End Option Parser ------#

#------- Setup Django Framework --------#
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from django.core.management import setup_environ
from kenya import settings

setup_environ(settings)

import backend.models as backend
import patients.tasks as tasks
import patients.models as patients

from transport_email import Transport as Email
#--------- End Django Framework ---------#

runner = tasks.message_runner(options)

#get clients 
if options.all or options.auto:
	runner.send_automated_messages()
if options.all or options.visits:
	runner.send_up_coming()
if options.all or options.resend:
	runner.send_repeat()

content = runner.content()

if options.email:
	subject = "Automatic Messages {auto} {visit} {resend}".format(**runner.values)

	Email.email(subject,content)
else:
	print content


