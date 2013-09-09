# Create your views here.

import sys

from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson
from django.shortcuts import get_object_or_404, render
from django.template import RequestContext

from patients import tasks 
from shujaa.forms import TestMessage
from shujaa import Transport 

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
	sys.stderr.flush()
	try:
		if request.method == "POST":
			sender = request.POST['source']
			message = request.POST['message']
			network = request.POST['network']
			messageID = request.POST['messageId']
			print >> sys.stderr, "Sujja Send"
			received = tasks.incoming_message(sender, message, network)
			http = "%s sent \"%s\" on %s (%s)\nReceived: %s"%(sender,message,network,messageID,received)
			print >> sys.stderr, http
			sys.stderr.flush()
			return HttpResponse(http)
		else:
			print >> sys.stderr, "SHUJAA GET RECIEVE"
			sys.stderr.flush()
			return HttpResponse("Please use post")
	except Exception as e:
		print >> sys.stderr, e
		sys.stderr.flush()

def testmessage(request):
	if request.method == 'POST': #submit
		form = TestMessage(request.POST) #bind new TestMessage form to post data
		if form.is_valid():
			to = request.POST['to']
			message = request.POST['message']
			Transport.send_shujaa(to,message,"safaricom")
			return HttpResponse("To: %s <br/> Message: %s"%(to,message))
	else:
		form = TestMessage() #unbound form
	return render(request,"test.html", {'form':form})
