import sys

# Create your views here.
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.utils.importlib import import_module
from django.conf import settings

from httpsms.forms import SendForm, SystemForm
from smssync.views import smssync
from httpsms.models import HTTPSMSOutgoing
from patients.models import Client, AutomatedMessage, Message, Nurse
import shujaa.views as shujaa



def httpSMS(request):
	#?start=id&end=id
	start = request.GET.get('start',0)
	end = request.GET.get('end',None)
	messages = HTTPSMSOutgoing.objects.all()[start:end]
	return render(request,'messages.html',{'messages':messages})
	
	
def sendSMS(request):
	if request.method == 'POST':
		form = SendForm(request.POST)
		if form.is_valid():
			new_request = HttpRequest()
			new_request.method = 'POST'
			post = {
				'callbackType':'incomingSms',
				'destination':'6873',
				'source':request.POST['sender_number'],
				'message':request.POST['content'],
				'messageID':SendForm.msgID(),
				'network':'safaricom'
				}
			new_request.POST = post
			print >> sys.stderr, post
			sys.stderr.flush()
			return shujaa.receive(new_request)
	form = SendForm()
	return render(request,'send.html',{'form':form})
	
def sendSystem(request):
	if request.POST:
		form = SystemForm(request.POST)
		if form.is_valid():
			transport = import_module(settings.TRANSPORT).Transport
			
			client = Client.objects.get(pk=request.POST['client'])
			data = {'last_name':client.last_name,'name':client.nickname,'sender':'Kinuthia'}
			message = AutomatedMessage.objects.get(pk=request.POST['message']).message.format(**data)
			
			Message(
				client_id=client,
				user_id=None,
				sent_by="System",
				content=message
			).save()
			
			transport.send(client.phone_number,message)
			
			return render(request,'system.html',{'form':form,'message':'Message Sent'})
		else:
			return render(request,'system.html',{'form':form})
	else:
		form = SystemForm()
		return render(request,'system.html',{'form':form})
	
