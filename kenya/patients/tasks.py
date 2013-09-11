import sys,re,random, datetime

from celery.schedules import crontab
from celery.task import group, periodic_task, task
from django.conf import settings
from django.utils.importlib import import_module

import patients.models as _patients #import Client, Message, Nurse
import backend.models as _backend

from transport_email import Transport as Email

@periodic_task(run_every=crontab())
def scheduled_tasks():
	last = _backend.AutoTask.objects.filter(function="scheduled_tasks").order_by('-pk')
	(date,hour) = last[0].data.split("|") if last else ("2013-07-01","19")
	if hour=="8":
		hour="13"
	elif hour=="13":
		hour="19"
	else:
		hour="8"
		date=datetime.datetime.strptime(date,"%Y-%m-%d")+datetime.timedelta(1)
		date = date.strftime("%Y-%m-%d")
	print "%s %s"%(date,hour)
	log("scheduled_tasks","|".join((date,hour)))

@task
def log(func,data=""):
	l = _backend.AutoTask(function=func,data=data)
	l.save()


'''
Todo: Move this to the recieve section
@periodic_task(run_every=crontab(minute=0, hour=0))
def update_all():
    """Updates all clients to see if they are urgent.

    """
    for client in Client.objects.all():
        update_client(client)


@task
def update_client(client):
    """A wrapper to let us update a client asynchronously.
    """
    client.update()
'''

'''
Todo: Rewrite
@periodic_task(run_every=crontab(minute=55, hour=16, day_of_week="wednesday"))
def send_all_scheduled():
    """Sends a reminder message to every client twice a week, unless there is
    no defined transport in settings.py.

    """
    transport = import_module(settings.TRANSPORT).Transport

    transport_kwargs = getattr(settings, 'TRANSPORT_KWARGS', {})
    batch = group([scheduled_message.subtask(args=(client,))
        for client in Client.objects.all()])
    messages = batch.apply_async().join()
    transport.send_batch(messages)


@task
def scheduled_message(client):
    """Calculates which message to send to a client, then sends it.

    Arguments:
    client - the client to send to

    Returns:
    A tuple in the form (phone number, message) for this client

    """
    week = int((date.today() - client.due_date).days / 7)
    messages = AutomatedMessage.objects.filter(
        condition__in=client.conditions.all(),
        start_week__lte=week,
        end_week__gte=week,
    )
    messages = [x for x in messages if x not in client.sent_messages.all()]
    
    content = ""
    if len(messages) == 0:
        content = "Error: please report this error to your clinic."
    else:
        message = messages[0]
        content = message.message
        if not message.repeats:
            client.sent_messages.add(message)
            client.save()

    Message(
        client_id=client,
        user_id=None,
        sent_by="System",
        content=content
    ).save()

    return (client.phone_number, content)
'''


def get_clients_to_message(clients=_patients.Client.objects.all(),now=datetime.datetime.now(),day=True,hour=True):
	"""
	Return all clients that should be messaged now
	"""
	#get clients for current time
	#minus those in the control group 
	#minus those who have finished or stopped
	clients = clients.exclude(study_group__name="control")\
	.exclude(pregnancy_status="Stopped").exclude(pregnancy_status="Finished")
	
	#if day and hour flags are set
	if(day):
		clients = clients.filter(send_day=now.weekday())
		if(hour):
			clients = clients.filter(send_time__range=(now.hour-1,now.hour+1))
	return clients
	
def get_message(client,now=datetime.datetime.now()):
	"""
	Return (if any) the correct message to send the client at this time.
	"""
	
	base_lookup = {b.name:b for b in _backend.MessageBase.objects.all()}
	normal = _backend.Condition.objects.get(name="normal")
	
	condition = client.condition
	language = client.language
	study_group = client.study_group
	
	if client.pregnancy_status == "Pregnant":
		base = base_lookup['edd']
		offset = 40 - (client.due_date-now.date()).days/7
	elif client.pregnancy_status == "Post-Partum" and client.pregnancy_event.outcome != "miscarriage":
		base = base_lookup['dd']
		delivery_date = client.pregnancy_event.date
		offset = 40 - (now.date() - delivery_date).days/7
	
	#print >> sys.stderr, client,condition,language,study_group,base,offset
		
	message = _backend.AutomatedMessage.objects.filter(send_base=base,send_offset=offset)\
	.filter(groups__in=[condition]).filter(groups__in=[language]).filter(groups__in=[study_group])
	
	#print len(message)
	if len(message)==0: 
		#no message was found get message for normal conditon
		message = _backend.AutomatedMessage.objects.filter(send_base=base,send_offset=offset)\
	.filter(groups__in=[normal]).filter(groups__in=[language]).filter(groups__in=[study_group])
	
	messages_to_send = []
	for m in message:
		messages_to_send.append(m.message)
		
	return messages_to_send
	
def get_upcomming_visit_clients(now=datetime.datetime.now()):
	pass
	
def get_upcomming_visit_message(client):
	pass
	
def get_missed_visit_client(now=datetime.datetime.now()):
	pass
	
def get_missed_visit_message(client):
	pass



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
	#transport logging
	import logging
	transport_logger = logging.getLogger("logview.transport")
	transport_logger.info('send,%s,%s,%s,%s,"%s",%s'%
	(client.phone_number,client.id,client.last_name,client.first_name,content,sender))
	
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


def incoming_message(phone_number, message,network="safaricom"):
	"""Adds an incoming message to the database.
	"""
	
	#transport logging
	import logging
	transport_logger = logging.getLogger("logview.transport")
	transport_logger.info('recieved,%s,"%s",%s'%(phone_number,message,network))
	print >> sys.stderr, 'recieved,%s,"%s",%s'%(phone_number,message,network)
	
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
					client.phone_network = network 
					client.validated = True
					client.save()
					return True
		#if the the message is not a valid key
		Email.template_email('number_not_found',**{'phone_number':phone_number,'message':message})
		return False
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
		client.last_msg = datetime.date.today()
		return True
