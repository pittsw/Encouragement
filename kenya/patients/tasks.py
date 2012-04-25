from datetime import timedelta
import logging

from celery.schedules import crontab
from celery.task import periodic_task, task
from django.conf import settings

from patients.models import Client

@periodic_task(run_every=crontab(minute=0, hour=12, day_of_week="1,4"))
def send_all():
    """Sends a reminder message to every client twice a week, unless there is
    no defined transport in settings.py.

    """
    transport = settings.TRANSPORT
    if transport is None:
        return

    transport_kwargs = settings.TRANSPORT_KWARGS
    for client in Client.objects.all():
        task_wrapper.delay(transport.send, client, **transport_kwargs)

@task
def task_wrapper(f, *args, **kwargs):
    f(args, kwargs)


@periodic_task(run_every=timedelta(seconds=30))
def poll():
    """Polls the transport defined in settings.py, if one is defined.

    """
    transport = settings.TRANSPORT
    if transport is None:
        return

    transport_kwargs = settings.TRANSPORT_KWARGS
    transport.poll(**transport_kwargs)

