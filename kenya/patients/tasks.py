from datetime import date, datetime, timedelta
import sys

from celery.schedules import crontab
from celery.task import group, periodic_task, task
from django.conf import settings
from django.utils.importlib import import_module

from patients.models import AutomatedMessage, Client, Message, Nurse


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


def message_client(client, nurse, sender, content, transport=None,
                   transport_kwargs={}):
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
	content = content%{'nickname':client.nickname,'first_name':client.first_name,'last_name':client.last_name,'next_visit':client.next_visit,'nurse':nurse_name}
	
    Message(
        client_id=client,
        user_id=nurse,
        sent_by=sender,
        content=content,
    ).save()
    transport.send(client, content, **transport_kwargs)


def incoming_message(phone_number, message):
    """Adds an incoming message to the database.

    """
    clients = Client.objects.filter(phone_number=phone_number)
    if len(clients) == 0:
        # We got a message from someone without a registered phone number
        return add_client(phone_number, message)
        

    client = clients[0]
    Message(
        client_id=client,
        user_id=Nurse.objects.all()[0],
        sent_by='Client',
        content=message,
        date=datetime.now(),
    ).save()

    return True


def add_client(phone_number, message):
    """When a client is added, we add everything except their phone number.
    When the client texts a certain code, this is matched up and their phone
    number is added.

    """
    unregistared_clients = Client.objects.filter(phone_number="")

    for client in unregistared_clients:
        if message == client.generate_key():
            client.phone_number = phone_number
            client.save()
            return True
    return False
