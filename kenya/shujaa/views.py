# Create your views here.

import sys

from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson

from patients.tasks import incoming_message
from shujaa.models import ShujaaOutgoing

@csrf_exempt
def smssync(request):
    print >> sys.stderr, "SMSSYNC!?"
    sys.stderr.flush()
    try:
        with transaction.commit_on_success():
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

@csrf_exempt
def print_request(request):
	http = "Print Page<br>\n"
	http += "Post<br>\n"
	for k in request.POST.iteritems():
		http+="*%s->%s<br>\n"%(k)
		print >> sys.stderr, "*%s->%s<br>"%(k)
	http += "Get<br>\n"
	for k in request.GET.iteritems():
		http+="*%s->%s<br>\n"%(k)
		print >> sys.stderr, "*%s->%s<br>"%(k)
	sys.stderr.flush()
	return HttpResponse(http)

@csrf_exempt
def receive(request):
	try:
		with transaction.commit_on_success():
			if request.method == "POST":
				sender = request.POST['source']
				message = request.POST['message']
				network = request.POST['network']
				messageID = request.POST['messageID']
				received = incoming_message(sender, message)
				http = "%s sent \"%s\" on %s (%s)\nReceived: %s"%(sender,message,network,messageID,received)
				return HttpResponse(http)
	except Exception as e:
		 print >> sys.stderr, "Exception: {e}".format(e=e)
        sys.stderr.flush()
