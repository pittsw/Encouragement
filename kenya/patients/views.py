from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

from patients.forms import ClientForm, MessageForm
from patients.models import Client, Message, Location, Nurse, SMSSyncOutgoing
from patients.tasks import incoming_message

def over(request):
	return render_to_response("frame.html")

def DoesNotExist(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def client(request, id_number):
	try:
		client = Client.objects.get(id=id_number)
		messages = Message.objects.filter(client_id=client)
		return render_to_response("display.html", {"client":client, "messages":messages})
	except DoesNotExist:
		return render_to_response("form.html")
		
def detail(request, id_number):
	try:
		client = Client.objects.get(id=id_number)
		messages = Message.objects.filter(client_id=client)
		return render_to_response("detail.html", {"client":client, "messages":messages})
	except DoesNotExist:
		return render_to_response("form.html")
	
def list_clients(request):
	clients = Client.objects.all()
	return render_to_response("list.html", {"clients":clients})

@csrf_exempt
def add_client(request):
	if request.method == 'POST':
		form = ClientForm(request.POST)
		if form.is_valid():
			f = form.save()
		return HttpResponseRedirect('/add/')
	else:
		form = ClientForm()
		return render_to_response("form.html", {
		"form": form,
		})
    
@csrf_exempt
def add_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            f = form.save()
        return HttpResponseRedirect('/message/')
    else:
        form = MessageForm()
        return render_to_response("message.html", {
        "form": form,
        })

@csrf_exempt
def smssync(request):
    secret = settings.SMSSYNC_SECRET
    payload = {
        "secret": secret,
    }

    if request.method == 'POST':
        sender = request.POST['from']
        msg = request.POST['message']
        payload['success'] = "true" if incoming_message(sender, msg) else "false"

    outgoing_messages = SMSSyncOutgoing.objects.all()
    if len(outgoing_messages) > 0:
        payload['task'] = "send"
        messages = [{
            "to": msg.target,
            "message": msg.content,
        } for msg in outgoing_messages]

        if 'SMSSync' in request.META['HTTP_USER_AGENT']:
            outgoing_messages.delete()
        payload['messages'] = messages

    reply = {
        "payload": payload
    }
    return HttpResponse(simplejson.dumps(reply), mimetype="application/json")
