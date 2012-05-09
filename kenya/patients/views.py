from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext

from patients.forms import AddClientForm, ClientForm, MessageForm
from patients.models import Client, Message, Location, Nurse, SMSSyncOutgoing
from patients.tasks import incoming_message, message_client

def over(request):
    return render_to_response("frame.html")

def DoesNotExist(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

@csrf_exempt
def client(request, id_number):
    if request.method == 'POST':
        client = Client.objects.get(id=id_number)
        nurse = Nurse.objects.get(user=request.user)
        message_client(client, nurse, 'Nurse', request.POST['text'])
        messages = Message.objects.filter(client_id=client)
        return render_to_response("display.html", {"client":client, "messages":messages}, context_instance=RequestContext(request))
    else:
        client = Client.objects.get(id=id_number)
        messages = Message.objects.filter(client_id=client)
        return render_to_response("display.html", {"client":client, "messages":messages}, context_instance=RequestContext(request))
        
def detail(request, id_number):
    try:
        client = Client.objects.get(id=id_number)
        messages = Message.objects.filter(client_id=client)
        return render_to_response("detail.html", {"client":client, "messages":messages}, context_instance=RequestContext(request))
    except DoesNotExist:
        return render_to_response("form.html")
    
def list_clients(request):
    clients = Client.objects.all()
    form = AddClientForm()
    return render_to_response("list.html", {"clients":clients, "form": form}, context_instance=RequestContext(request))

def add_client(request):
    form = None
    if request.method == "GET":
        form = AddClientForm()
    elif request.method == "POST":
        if request.POST.get("submit", ""):
            form = AddClientForm(request.POST)
            if form.is_valid():
                id = form.cleaned_data['id']
                client = form.save(commit=False)
                client.id = id
                client.save()
                return list_clients(request)
        else:
            return list_clients(request)
    c = {
        'form': form
    }
    c.update(csrf(request))
    return render_to_response('form.html', c, context_instance=RequestContext(request))


def edit_client(request, id):
    client = get_object_or_404(Client, id=id)
    form = None
    if request.method == "GET":
        form = ClientForm(instance=client)

    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if request.POST.get("submit", ""):
            # They clicked submit
            if form.is_valid():
                form.save()
                return detail(request, id)
        else:
            return detail(request, id)
    c = {
        "form": form,
    }
    c.update(csrf(request))
    return render_to_response("edit_client.html", c,
                              context_instance=RequestContext(request))
    
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
