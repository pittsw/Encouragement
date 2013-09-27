import sys,re,random, datetime

from celery.schedules import crontab
from celery.task import group, periodic_task, task
from django.conf import settings
from django.utils.importlib import import_module
from django.db.models import F,Q

import patients.models as _patients #import Client, Message, Nurse
import backend.models as _backend

from transport_email import Transport as Email

class message_runner:
	
	def __init__(self,options):
		#options
		self.day = options.day
		self.hour = options.hour
		self.send = options.send
		self.now = options.time
		
		#vars
		self.base_lookup = {b.name:b for b in _backend.MessageBase.objects.all()}
		self.values = {
			"auto":0,"visit":0,"resend":0,
			}
	
	def send_automated_messages(self,clients=_patients.Client.objects.all()):
		"""
		Return all clients that should be messaged now
		"""
		#filter out clients who should not recieve a message
		clients = self.exlude_clients(clients)
		
		#if day and hour flags are set
		#get clients for current time
		if(self.day):
			clients = clients.filter(send_day=self.now.weekday())
			if(self.hour):
				closest_hour = 8 if self.now.hour <=9 else 13 if self.now.hour <=14 else 19
				clients = clients.filter(send_time=(closest_hour))
		
		print "Found %i clients to message."%clients.count()
		
		for client in clients:
			self.send_one_automated_message(client)
		self.values['auto'] = clients.count()
	
	def send_up_coming(self,clients=_patients.Client.objects.all(),days=2):
		"""
		Return all clients who have an upcoming clinic visit
		"""
		#filter out clients who should not recieve a message
		clients = self.exlude_clients(clients)
		
		#if hour flag is set
		if(self.hour):
			closest_hour = 8 if self.now.hour <=9 else 13 if self.now.hour <=14 else 19
			clients = clients.filter(send_time=(closest_hour))
		
		#get clients with a visit in the days in the future.
		clients = clients.filter(next_visit=self.now+datetime.timedelta(days=days))
		
		print "Found %i clients who are comming in %i days."%(clients.count(),days)
		
		for client in clients:
			#get client pregnancy status and week offset
			if client.pregnancy_status == "Pregnant":
				base = self.base_lookup['upcoming_anc']
			elif client.pregnancy_status == "Post-Partum" and client.pregnancyevent.outcome != "miscarriage":
				base = self.base_lookup['upcoming_pnc']
				
			messages = self.get_message(client,base,0,groups=False)
			for m in messages:
				self.print_message(m.message)
				if self.send:
					print "Sending..."
					message_client(client,None,"System",m.message)
		
		self.values['visit'] = clients.count()
		
	def send_repeat(self,clients=_patients.Client.objects.all(),days=2):
		#if hour flag is set
		if(self.hour):
			closest_hour = 8 if self.now.hour <=9 else 13 if self.now.hour <=14 else 19
			clients = clients.filter(send_time=(closest_hour))
		
		#get two way clients who have not responded within two days
		#and last system message was over 2 days ago
		clients = clients.filter(Q(last_msg_client=None) | Q(last_msg_client__lt=\
		F('last_msg_system')-datetime.timedelta(days=days))).filter(last_msg_system__lt=\
		datetime.date.today()-datetime.timedelta(days=days),study_group__name='two_way')
		
		print "Found %i clients who have not responded with in %i days."%(clients.count(),days)
		
		if self.send: #increase the repeat_msg count
			clients.update(F('repeat_msg')+1)
			
		for client in clients:
			self._now = self.now
			self.now = self.now-datetime.timedelta(days=client.repeat_msg*days)
			self.send_one_automated_message(client)
			self.now = self._now
			
		self.values['resend'] = clients.count()

	def print_message(self,msg,l=50,first=True,tabs=2):
		if first:
			print "%s* (%i)%s"%('\t'*tabs,len(msg),msg[:l])
		else:
			print '\t'*tabs+msg[:l]
		if l<len(msg):
			self.print_message(msg[l:],first=False)
		else:
			print ''
			
	def send_one_automated_message(self,client):
		#get client pregnancy status and week offset
		if client.pregnancy_status == "Pregnant":
			base = self.base_lookup['edd']
			offset = 40 - (client.due_date-self.now.date()).days/7
		elif client.pregnancy_status == "Post-Partum":
			base = self.base_lookup['dd']
			offset = (self.now.date() - client.pregnancyevent.date).days/7
		
		messages = self.get_message(client,base,offset)
		for m in messages:
			self.print_message(m.message)
			if self.send :
				print "Sending..."
				message_client(client,None,"System",m.message)
				client.last_msg_system = datetime.date.today()
				client.save()
				
	def get_message(self,client,base,offset,groups=True):
		"""
		Return (if any) the correct message to send the client at this time.
		-- groups: flag to filter messages based on condition and study_group
		"""
		
		condition = client.condition
		language = client.language
		study_group = client.study_group
		
		print >> sys.stderr, client,condition,language,study_group,base,offset
			
		message = _backend.AutomatedMessage.objects.filter(send_base=base,send_offset=offset).filter(groups__in=[language])
		
		if groups:
			message = message.filter(groups__in=[condition]).filter(groups__in=[study_group])
			if message.count()==0: 
				#no message was found get message for normal conditon
				message = _backend.AutomatedMessage.objects.filter(send_base=base,send_offset=offset)\
			.filter(groups__name__in=['normal']).filter(groups__in=[language]).filter(groups__in=[study_group])
		
		return message
		
	def exlude_clients(self,clients,one_way=True):
		#minus those in the control group 
		#minus those who have finished or stopped
		#minus those who have had a mis-carrage
		clients = clients.exclude(study_group__name="control")\
		.exclude(pregnancy_status="Stopped").exclude(pregnancy_status="Finished")\
		.exclude(pregnancyevent__outcome="miscarriage")
		
		if one_way==False:
			clients = clients.exclude(study_group__name="one_way")
		return clients

	def content(self):
		return 	"""
	Mobil Watch Automatic Messages Sent: {0.now}
		Automated: {0.values[auto]}
		Visit:{0.values[visit]}
		Resent:{0.values[resend]}

		Options:
			Day: {0.day} Hour: {0.hour} Send: {0.send}""".format(self)
			
	def __str__(self):
		return "Now: {0.now} Day: {0.day} Hour: {0.hour} Send: {0.send}".format(self)

def message_client(client, nurse, sender, content, transport=None,transport_kwargs={}):
	"""Sends the given message to the client.

	Arguments:
	client - a _patients.models.Client object, representing the client
			 to send to
	nurse - a _patients.models.Nurse object, representing the nurse
			who sent the message (or the special Nurse object
			'System')
	sender - 'Nurse' or 'System'
	content - the message to send (a string)
	transport - an object/class/whatever that has can be called with
				transport.send
	transport_kwargs - a dict containing any arguments the transport
					   might need

	"""
	
	if client.study_group.name=='control':
		return #do not send a message if control group

	if transport is None:
		transport = import_module(settings.TRANSPORT).Transport
	
	#replace message variables 
	nurse_name = nurse.user.first_name if nurse else settings.DEFAULT_NURSE_NAME
	content = content.format(name=client.nickname.capitalize())

	_patients.Message(
		client_id=client,
		user_id=nurse,
		sent_by=sender,
		content=content,
	).save()
	
	transport.send(client, content, **transport_kwargs)
	
	#transport logging
	#import logging
	#transport_logger = logging.getLogger("logview.transport")
	#transport_logger.info('send,%s,%s,%s,%s,"%s",%s'%
	#(client.phone_number,client.id,client.last_name,client.first_name,content,sender))


def incoming_message(phone_number, message,network="safaricom"):
	"""Adds an incoming message to the database.
	"""
	
	#transport logging
	import logging
	#transport_logger = logging.getLogger("logview.transport")
	#transport_logger.info('recieved,%s,"%s",%s'%(phone_number,message,network))
	#print >> sys.stderr, 'recieved,%s,"%s",%s'%(phone_number,message,network)
	
	clients = _patients.Client.objects.filter(phone_number=phone_number)
	if len(clients) == 0:
		# recieved a message from a phone number not in database
		if len(message.strip()) == 5: #compare to key length in patients.models
			message = message.strip().upper()
			#check if message is equal to a valid key
			for client in _patients.Client.objects.filter():
				if message == client.generate_key():
					if client.validated: #new number for already valid client
						Email.template_email('valid_repeat',**{'client':client,'phone_number':phone_number,'network':network,"message":message})
						return False
					Email.template_email('number_change',**{'client':client,'phone_number':phone_number,'network':network,"message":message})
					#update phone number and network
					client.phone_number = phone_number 
					#client.phone_network = network #Don't change network since we aren't using Artiel
					client.validated = True
					client.save()
					return True
		#if the the message is not a valid key
		Email.template_email('number_not_found',**{'phone_number':phone_number,'message':message})
		return False
	#recieved a message from a phone number in the database
	else:
		client = clients[0]
		if len(message.strip()) == 5 and message.strip().upper() == client.generate_key():
			client.validated = True
			client.save()
			return True
		if re.match("^[S7]\s*[T8]\s*[O6]\s*[P7]$",message.strip().upper()):
			Email.template_email('dropped',**{'client':client})
			client.pregnancy_status = "Stopped"
			client.save()
			return True
		_patients.Message(
			client_id=client,
			user_id=None,
			sent_by='Client',
			content=message,
		).save()
		client.last_msg_client = datetime.date.today()
		client.repeat_msg = 0
		client.save()
		return True
