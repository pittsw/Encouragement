from datetime import date, datetime, timedelta
import sys

from celery.schedules import crontab
from celery.task import periodic_task, task
from django.conf import settings

from patients.models import AutomatedMessage, Client, Message, Nurse
import patients.transports


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
def send_all():
    """Sends a reminder message to every client twice a week, unless there is
    no defined transport in settings.py.

    """
    transport = getattr(
        sys.modules['patients.transports'],
        settings.TRANSPORT,
        None
    )
    if transport is None:
        return

    transport_kwargs = getattr(settings, 'TRANSPORT_KWARGS', {})
    for client in Client.objects.all():
        scheduled_message.delay(client, transport, transport_kwargs)


@task
def scheduled_message(client, transport=None, transport_kwargs={}):
    """Calculates which message to send to a client, then sends it.

    Arguments:
    client - the client to send to
    transport - the transport to send through
    transport_kwargs - a dict containing options for the transport

    """
    week = int((date.today() - client.due_date).days / 7)
    messages = AutomatedMessage.objects.filter(
        condition__in=client.conditions.all(),
        start_week__lte=week,
        end_week__gte=week,
    )
    messages = [x for x in messages if x not in client.sent_messages.all()]
    
    if len(messages) == 0:
        return {
			'week': week,
			'messages': messages,
        }
        
    message = messages[0]
    if not message.repeats:
        client.sent_messages.add(message)
        client.save()
    message_client(client, None, 'System',
                   message.message, transport, transport_kwargs)
    return {
		'week': week,
		'messages': messages,
    }


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
        transport = getattr(
            sys.modules['patients.transports'],
            settings.TRANSPORT,
            None
        )
        if transport is None:
            return

    Message(
        client_id=client,
        user_id=nurse,
        sent_by=sender,
        content=content,
        date=datetime.now()
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
