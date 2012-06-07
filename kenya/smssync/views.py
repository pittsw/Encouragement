import sys

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson

from patients.tasks import incoming_message
from smssync.models import SMSSyncOutgoing

@csrf_exempt
def smssync(request):
    try:
        secret = settings.SMSSYNC_SECRET
        payload = {
            "secret": secret,
        }

        if request.method == 'POST':
            sender = request.POST['from']
            msg = request.POST['message']
            print >> sys.stderr, "{sender}: {msg}".format(sender=sender, msg=msg)
            sys.stderr.flush()
            payload['success'] = "true" if incoming_message(sender, msg) else "false"
        else:
            print >> sys.stderr, "GET!?"
            sys.stderr.flush()

        outgoing_messages = SMSSyncOutgoing.objects.all()
        if len(outgoing_messages) > 0:
            payload['task'] = "send"
            messages = [{
                "to": msg.target,
                "message": msg.content,
            } for msg in outgoing_messages]

            if ('HTTP_USER_AGENT' not in request.META
                    or 'SMSSync' in request.META['HTTP_USER_AGENT']):
                outgoing_messages.delete()
            payload['messages'] = messages

        reply = {
            "payload": payload
        }
        return HttpResponse(simplejson.dumps(reply), mimetype="application/json")
    except Exception as e:
        print >> sys.stderr, "Exception: {e}".format(e=e)
        sys.stderr.flush()
        return HttpResponse(str(e))
