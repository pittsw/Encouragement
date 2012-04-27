from datetime import datetime, timedelta
import sys

from celery.schedules import crontab
from celery.task import periodic_task, task
from django.conf import settings

from patients.models import Client, Message, Nurse
import patients.transports

@periodic_task(run_every=crontab(minute=0, hour=12, day_of_week="1,4"))
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

    print transport

    transport_kwargs = getattr(settings, 'TRANSPORT_KWARGS', {})
    for client in Client.objects.all():
        message_client.delay(client, 'System', transport_kwargs, transport)

@task
def message_client(client, sender, transport_kwargs, transport=None):
    """Calculates which message should be sent to the given client,
    then sends it via the transport.

    """
    if transport is None:
        transport = getattr(
            sys.modules['patients.transports'],
            settings.TRANSPORT,
            None
        )
        if transport is None:
            return

    content = "Thanks for using Encouragement!"
    Message(
        client_id=client,
        user_id=Nurse.objects.all()[0],
        sent_by=sender,
        content=content,
        date=datetime.now()
    ).save()
    transport.send(client.phone_number, content, **transport_kwargs)

def incoming_message(phone_number, message):
    """Adds an incoming message to the database.

    """
    clients = Client.objects.filter(phone_number=phone_number)
    if len(clients) != 1:
        # We got a message from someone who isn't registered
        return False

    Message(
        client_id=clients[0],
        user_id=Nurse.objects.all()[0],
        sent_by='Client',
        content=message,
        date=datetime.now()
    ).save()
    return True
