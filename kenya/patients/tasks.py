from datetime import date, datetime, timedelta
import sys

from celery import group
from celery.schedules import crontab
from celery.task import periodic_task, task
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
    batch = group([scheduled_message.s(client, transport, transport_kwargs)
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
    
    if len(messages) == 0:
        return (client.phone_number, "Error: please contact clinic")
        
    message = messages[0]
    if not message.repeats:
        client.sent_messages.add(message)
        client.save()

    Message(
        client_id=client,
        user_id=None,
        sent_by="System",
        content=message.message
    ).save()

    return (client.phone_number, message.message)


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

    Message(
        client_id=client,
        user_id=nurse,
        sent_by=sender,
        content=content,
    ).save()
    transport.send(client.phone_number, content, **transport_kwargs)


def incoming_message(phone_number, message):
    """Adds an incoming message to the database.

    """
    clients = Client.objects.filter(phone_number=phone_number)
    if len(clients) == 0:
        # We got a message from someone without a registered phone number
        add_client(phone_number, message)
        return

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
    clients = Client.objects.filter(phone_number="")

    for client in clients:
        if message == client.generate_key():
            client.phone_number = phone_number
            client.save()
