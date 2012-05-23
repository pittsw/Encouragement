from csv import DictWriter

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

from patients.forms import AddClientForm, ClientForm, MessageForm, VisitForm
from patients.models import *
from patients.tasks import incoming_message, message_client

@login_required
def index(request):
    form = render_to_string("add_client.html", {"form": AddClientForm()},
        context_instance=RequestContext(request))
    clients = Client.objects.all()
    listf = render_to_string("list_fragment.html", {'clients': clients})
    c = {
        'form': form,
        'listf' : listf,
    }
    c.update(csrf(request))
    return render_to_response("test.html", c, context_instance=RequestContext(request))

def DoesNotExist(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def client(request, id_number):
    if request.method == 'POST':
        client = Client.objects.get(id=id_number)
        if request.POST['text']:
            nurse = Nurse.objects.get(user=request.user)
            message_client(client, nurse, 'Nurse', request.POST['text'])
        messages = Interaction.objects.filter(client_id=client)
        return render_to_response("display.html", {"client":client, "messages":messages}, context_instance=RequestContext(request))
    else:
        client = Client.objects.get(id=id_number)
        messages = Interaction.objects.filter(client_id=client)
        return render_to_response("display.html", {"client":client, "messages":messages}, context_instance=RequestContext(request))

def message_fragment(request, id):
    client = Client.objects.get(id=id)
    messages = Interaction.objects.filter(client_id=client)
    for message in messages:
        try:
            message.message.read = True
            message.message.save()
        except Message.DoesNotExist:
            continue
    client.update()
    return render_to_response("message_frag.html", {"client": client, "messages":messages}, context_instance=RequestContext(request))

def message_list_frag(request, id):
    client = Client.objects.get(id=id)
    messages = Interaction.objects.filter(client_id=client)
    for message in messages:
        try:
            message.message.read = True
            message.message.save()
        except Message.DoesNotExist:
            continue
    client.update()
    return render_to_response("message_listmode.html", {"client": client, "messages":messages}, context_instance=RequestContext(request))
        
def detail(request, id_number):
    try:
        client = Client.objects.get(id=id_number)
        notes = Note.objects.filter(client_id=client)
        history = Visit.objects.filter(client_id=client)
        fragment = render_to_string("client_fragment.html", {"client":client})
        visit_form = render_to_string("visit_form.html", {"form": VisitForm()})
        return render_to_response("detail.html", {
            "client": client,
            "notes": notes,
            "history": history,
            "fragment": fragment,
            "form": visit_form,
        }, context_instance=RequestContext(request))
    except DoesNotExist:
        return render_to_response("form.html")
    
def list_clients(request):
    clients = Client.objects.all()
    return render_to_response("list.html", {"clients":clients}, context_instance=RequestContext(request))

def add_note(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == "POST":
        nurse = Nurse.objects.get(user=request.user)
        n = Note(client_id=client, author_id=nurse, content=request.POST.get("text"))
        n.save()
        return HttpResponse('')
    return render_to_response("add_note.html", {"client":client}, context_instance=RequestContext(request))


def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        note.delete()
        return HttpResponse('')


def add_visit(request, id):
    form = None
    client = get_object_or_404(Client, id=id);
    if request.method == "GET":
        form = VisitForm()
    elif request.method == "POST":
        form = VisitForm(request.POST)
        if form.is_valid():
            comments = form.cleaned_data['comments']
            date = form.cleaned_data['date']
            Visit(client_id=client, comments=comments, date=date).save()
            form = VisitForm()
            return HttpResponse('')
    return render_to_response('visit_form.html', {'form': form})

def delete_visit(request, pk):
    visit = get_object_or_404(Visit, pk=pk)
    if request.method == "POST":
        visit.delete()
        return HttpResponse('')

def add_client(request):
    form = None
    c = {}
    if request.method == "GET":
        form = AddClientForm()
    elif request.method == "POST":
        form = AddClientForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['id']
            client = form.save(commit=False)
            client.id = id
            client.save()
            return HttpResponse('')
    return render_to_response("add_client.html", {'form': form},
                              context_instance=RequestContext(request))


def client_fragment(request, id):
    client = get_object_or_404(Client, id=id)
    return render_to_response("client_fragment.html", {'client': client},
                              context_instance=RequestContext(request))

def list_fragment(request, id_number):
    clients = Client.objects.all().exclude(id=id_number)
    top_client = Client.objects.get(id=id_number)
    clients = [top_client] + [x for x in clients]
    return render_to_response("list_fragment.html", {'clients': clients},
                              context_instance=RequestContext(request))

def edit_client(request, id):
    client = get_object_or_404(Client, id=id)
    form = None
    if request.method == "GET":
        form = ClientForm(instance=client)

    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return HttpResponse('')
    c = {
        "form": form,
    }
    return render_to_response("edit_client.html", c,
                              context_instance=RequestContext(request))
    
def add_message(request, id_number):
    if request.method == 'POST':
        text = request.POST['text']
        nurse = Nurse.objects.get(user=request.user)
        client = get_object_or_404(Client, id=id_number)
        message_client(client, nurse, 'Nurse', text)
        return HttpResponse('')

def add_call(request, id_number):
    if request.method == "POST":
        nurse = Nurse.objects.get(user=request.user)
        client = get_object_or_404(Client, id=id_number)
        content = request.POST['content']
        duration = request.POST['duration']
        try:
            duration = int(duration)
        except ValueError:
            duration = 0
        PhoneCall(
            user_id=nurse,
            client_id=client,
            content=content,
            duration=duration,
        ).save()
    return HttpResponse('')

def csv_helper(**filter_kwargs):
    field_list = ['id', 'last_name', 'first_name', 'phone_number', 'birth_date',
        'location_id', 'pregnancy_status', 'due_date', 'years_of_education']
    clients = Client.objects.all().order_by('id').filter(**filter_kwargs).values(*field_list)
    field_list += ['location', 'conditions']
    field_list.remove('location_id')
    response = HttpResponse(';'.join(field_list) + "\n", mimetype="text/csv")
    locations = dict([(loc.pk, loc.name) for loc in Location.objects.all()])
    conditions = dict([(cond.pk, cond.name) for cond in Condition.objects.all()])
    writer = DictWriter(response, field_list, delimiter=";")
    for client in clients:
        client_obj = Client.objects.get(id=client['id'])
        client['location'] = locations[client['location_id']]
        del client['location_id']
        client['conditions'] = [conditions[x.pk] for x in client_obj.conditions.all()]
        writer.writerow(client)
    response['Content-Disposition'] = ('attachment; filename=clients.csv')
    return response

def csv(request):
    return csv_helper()

def clientcsv(request, id_number):
    return csv_helper(id=id_number)

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
