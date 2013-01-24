# Create your views here.

import sys

from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson

from patients import tasks 

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
	print >> sys.stderr, "RECEIVING!!"
	sys.stderr.flush()
	try:
		with transaction.commit_on_success():
			if request.method == "POST":
				sender = request.POST['source']
				message = request.POST['message']
				network = request.POST['network']
				messageID = request.POST['messageId']
				received = tasks.incoming_message(sender, message)
				http = "%s sent \"%s\" on %s (%s)\nReceived: %s"%(sender,message,network,messageID,received)
				print >> sys.stderr, http
				sys.stderr.flush()
				return HttpResponse(http)
			else:
				print >> sys.stderr, "SHUJAA GET RECIEVE"
				sys.stderr.flush()
				return HttpResponse("Please use post")
	except Exception as e:
		print >> sys.stderr, "Exception: {e}".format(e=e)
		sys.stderr.flush()
