#------- Setup up Option Parser ------#
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-s","--send",action="store_true",help="flag to send messages",default=False)
parser.add_option("-a","--ask",action="store_false",help="flag to ask before sending each",default=True)
parser.add_option("-d","--day",action="store_true",help="flag to send messages for today only",default=False)
parser.add_option("-H","--hour",action="store_true",help="flag to send messages for this hour only",default=False)
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

def print_message(msg,l=50,first=True,tabs=2):
	if first:
		print "%s* (%i)%s"%('\t'*tabs,len(msg),msg[:l])
	else:
		print '\t'*tabs+msg[:l]
	if l<len(msg):
		print_message(msg[l:],first=False)

def yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,"y":True,"ye":True,"no":False,"n":False}
    if default == None:
        prompt = " [y/n] "
    elif default.lower() == "yes":
        prompt = " [Y/n] "
    elif default.lower() == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

#get clients 
clients = tasks.get_clients_to_message(day=options.day,hour=options.hour)

print "Found %i clients to message."%clients.count()
for c in clients:
	print "\t%s"%c
	messages = tasks.get_message(c)
	for m in messages:
		print_message(m)
		if options.send :
			if options.ask: #ask user if this message should be sent
				prompt = yes_no("Send?")
				if prompt==False:
					continue #do not send this message 
			print "Sending..."
			tasks.message_client(c,None,"System",m)
	


