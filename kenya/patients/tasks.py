from datetime import date, datetime, timedelta
import sys,re,random

from celery.schedules import crontab
from celery.task import group, periodic_task, task
from django.conf import settings
from django.utils.importlib import import_module

import patients.models as patients #import Client, Message, Nurse
import backend.models as backend
from transport_email import Transport as Email

@periodic_task(run_every=crontab())
def scheduled_tasks():
	last = backend.AutoTask.objects.filter(function="scheduled_tasks").order_by('-pk')
	(date,hour) = last[0].data.split("|") if last else ("2013-07-01","19")
	if hour=="8":
		hour="13"
	elif hour=="13":
		hour="19"
	else:
		hour="8"
		date=datetime.strptime(date,"%Y-%m-%d")+timedelta(1)
		date = date.strftime("%Y-%m-%d")
	now = datetime.strptime(date,"%Y-%m-%d")+timedelta(hours=int(hour))
	pregnant,post,visit = get_all_scheduled(now)
	print "%s (%s,%s,%s)"%(now,len(pregnant),len(post),len(visit))
	log("scheduled_tasks","|".join((date,hour)))

@task
def log(func,data=""):
	l = backend.AutoTask(function=func,data=data)
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

def get_all_scheduled(now=datetime.now()):
	
	pregnant,post,visit = [],[],[]
	for language in backend.LanguageGroup.objects.all():
		#filter based on language 
		m_language = backend.AutomatedMessage.objects.filter(groups=language)
		#exlude control subjects
		c_language = patients.Client.objects.filter(language=language).exclude(study_group__name="control")
		
		#get clients for this time
		c_language = c_language.filter(send_time__range=(now.hour-1,now.hour+1))
		
		#get clients for visit with in two days, only filtered on language and time
		for (client,message) in get_visit_messages(
			c_language.filter(next_visit=now.date()+timedelta(2)),
			m_language.filter(groups__name='visit',send_base__name="upcoming_anc"),now):
			patients.Message(client_id=client,user_id=None,sent_by="System",content=message.message).save()
			visit.append((client,message))
		
		#get clients for this day
		c_language = c_language.filter(send_day=now.weekday())
		
		for group in backend.StudyGroup.objects.exclude(name="control"):
			m_group = m_language.filter(groups=group)
			c_group = c_language.filter(study_group=group)
			
			for condition in backend.Condition.objects.all(): 
				#filter based on conditions 
				m_condition = m_group.filter(groups=condition)
				c_condition = c_group.filter(condition=condition)
				
				#process messages for before delivery
				for client in c_condition.filter(pregnancy_status="Pregnant"):
					week = (now.date() - client.due_date).days/7
					messages = m_condition.filter(send_base__name="edd",send_offset=week)
					for message in messages:
						patients.Message(client_id=client,user_id=None,sent_by="System",content=message.message).save()
						pregnant.append((client,message))
						
				#process messages for after delivery
				for client in c_condition.filter(pregnancy_status="Post-Partum"):
					try:
						delivery = patients.PregnancyEvent.objects.get(client=client)
						week = (now.date() - delivery.date).days/7
						messages = m_condition.filter(send_base__name="dd",send_offset=week)
						for message in messages:
							patients.Message(client_id=client,user_id=None,sent_by="System",content=message.message).save()
							post.append((client,message))
					except Exception, e:
						continue #no delivery event for client
	return (pregnant,post,visit)
	
def get_visit_messages(clients,messages_query,now):
	for client in clients:
		client_messages = messages_query.exclude(pk__in=patients.Message.objects.filter(client_id=client,automated_message__groups__name="visit"))
		if len(client_messages) == 0:
			client_messages = [random.choice(list(client_messages))]
		message = client_messages[0]
		yield (client,message)

def message_client(client, nurse, sender, content, transport=None,transport_kwargs={}):
	"""Sends the given message to the client.

	Arguments:
	client - a patients.models.Client object, representing the client
			 to send to
	nurse - a patients.models.Nurse object, representing the nurse
			who sent the message (or the special Nurse object
			'System')
	sender - 'Nurse' or 'System'
	content - the message to send (a string)
	transport - an object/class/whatever that has can be called with
				transport.send
	transport_kwargs - a dict containing any arguments the transport
					   might need

	"""
	if transport is None:
		transport = import_module(settings.TRANSPORT).Transport
	
	#replace message variables 
	nurse_name = nurse.user.first_name if nurse else settings.DEFAULT_NURSE_NAME
	content = content%{'name':client.nickname,'first_name':client.first_name,'last_name':client.last_name,'next_visit':client.next_visit,'nurse':nurse_name}

	patients.Message(
		client_id=client,
		user_id=nurse,
		sent_by=sender,
		content=content,
	).save()
	transport.send(client, content, **transport_kwargs)


def incoming_message(phone_number, message,network="default"):
	"""Adds an incoming message to the database.
	"""
	clients = patients.Client.objects.filter(phone_number=phone_number)
	if len(clients) == 0:
		# recieved a message from a phone number not in database
		if len(message.strip()) == 5: #compare to key length in patients.models
			message = message.strip().upper()
			#check if message is equal to a valid key
			for client in patients.Client.objects.filter():
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
		patients.Message(
			client_id=client,
			user_id=patients.Nurse.objects.all()[0],
			sent_by='Client',
			content=message,
		).save()
		client.last_msg = date.today()
		return True
