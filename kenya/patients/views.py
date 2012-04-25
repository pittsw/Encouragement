from django.shortcuts import render_to_response
from patients.models import Client, Message, Location, Nurse
from django.views.decorators.csrf import csrf_exempt
from patients.forms import ClientForm, MessageForm
from django.http import HttpResponseRedirect

def over(request):
	return render_to_response("frame.html")

def index(request):
	return render_to_response("index.html")

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
	except Page.DoesNotExist:
		return render_to_response("form.html")
	
def list_clients(request):
	clients = Client.objects.all()
	return render_to_response("list2.html", {"clients":clients})

@csrf_exempt
def add_client(request):
	if request.method == 'POST':
		form = ClientForm(request.POST)
		if form.is_valid():
			f = form.save()
		return HttpResponseRedirect('/kenya/add/')
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
        return HttpResponseRedirect('/kenya/message/')
    else:
        form = MessageForm()
        return render_to_response("message.html", {
        "form": form,
        })
