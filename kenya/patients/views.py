from csv import DictWriter
import sys, random, time
from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson

from patients.forms import AddClientForm, ClientForm, MessageForm, VisitForm
from patients.models import *
from patients.tasks import message_client

def get_object_or_default(klass, default, **kwargs):
    """Performs a get query, but instead of throwing an exception returns
    the default value if a matching object is not found.

    """
    try:
        return klass.objects.get(**kwargs)
    except:
        return default

@login_required
def index(request):
    clients = Client.objects.all().order_by("-study_group")
    patients = render_to_string("list_fragment.html", {'clients': clients})
    nurse = get_object_or_default(Nurse, "Administrator", user=request.user)
    c = {
        'patient_list': patients,
        'nurse': nurse,
    }
    c.update(csrf(request))
    return render_to_response("index.html", c, context_instance=RequestContext(request))

def DoesNotExist(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def message_fragment(request, id):
    client = Client.objects.get(id=id)
    client.pending = 0
    client.save()
    messages = Interaction.objects.filter(client_id=client)
    return render_to_response("message_frag.html", {"client": client, "messages":messages}, context_instance=RequestContext(request))

def message_list_frag(request, id):
    client = Client.objects.get(id=id)
    client.pending = 0
    client.save()
    messages = Interaction.objects.filter(client_id=client)
    return render_to_response("message_listmode.html", {"client": client, "messages":messages}, context_instance=RequestContext(request))

def client(request):
	if request.method == "GET":
		if "id" in request.GET:
			client = Client.objects.get(id=request.GET["id"])
			isList = request.GET.get('list')
			client.pending = 0
			client.save()
			messages = Interaction.objects.filter(client_id=client)
			if isList is None:
				message_fragment = render_to_string("message_frag.html", {"client": str(client), "messages":messages}, context_instance=RequestContext(request))
			else:
				message_fragment = render_to_string("message_listmode.html", {"client": str(client), "messages":messages}, context_instance=RequestContext(request))
			return render_to_response("display_client_fragment.html",
				{"client":client,
				"list":isList,
				"notes": Note.objects.filter(client_id=client),
				"history": Visit.objects.filter(client_id=client),
				"client_fragment": render_to_string("client_fragment.html", {"client":client}, context_instance=RequestContext(request)),
				"message_fragment":message_fragment,
				"visit_form": render_to_string("visit_form.html", {"form": VisitForm(),'client':client}, context_instance=RequestContext(request)),
				}, context_instance=RequestContext(request) )
	
	return render_to_response("display_client_fragment.html")

def add_note(request, id):
    client = get_object_or_404(Client, id=id)
    if request.method == "POST":
        nurse = get_object_or_default(Nurse, None, user=request.user)
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
        form = VisitForm(initial={"next_visit":client.next_visit})
    elif request.method == "POST":
        form = VisitForm(request.POST)
        if form.is_valid():
            comments = form.cleaned_data['comments']
            date = form.cleaned_data['date']
            Visit(client_id=client, comments=comments, date=date).save()
            form = VisitForm()
            return HttpResponse('')
    return render_to_response('visit_form.html', {'form': form,'client':client})

def delete_visit(request, pk):
    visit = get_object_or_404(Visit, pk=pk)
    if request.method == "POST":
        visit.delete()
        return HttpResponse('')

def add_client(request):
    form = None
    c = {}
    if request.method == "GET":
        next_month = (date.today() + timedelta(30)).strftime("%Y-%m-")
        due_date = (date.today() + timedelta(180)).strftime("%Y-%m-")
        form = AddClientForm(initial={"birth_date":"1990-","due_date":due_date,"next_visit":next_month,"conditions":"1",
        "previous_pregnacies":"1","living_children":"0","years_of_education":"1","phone_number":"254","pri_contact_number":"254",
        "sec_contact_number":"254",})
    elif request.method == "POST":
		form = AddClientForm(request.POST)
		if form.is_valid():
			id = form.cleaned_data['id']
			client = form.save(commit=False)
			client.id = id
			#client.study_group = study_group()
			client.save()
			'''
			Send initial message if any
			'''
			message = AutomatedMessage.objects.filter(send_base__exact="signup").filter(send_offset__exact=0) #get messages sent 0 days from signup
			if message.count() > 0:
				text = message[0].message
				sender = "System"
				nurse = None
				message_client(client,nurse,sender,text) #send initial message to client
			
			return HttpResponse(str(client.id))
    return render_to_response("add_client.html", {'form': form},
                              context_instance=RequestContext(request))
'''
Select which of three groups the new client should be in
2: Messaging that require two way communication
1: Push messaging not requiring any responce
0: Control group - sent no messages
'''                              
def study_group():
	return random.randint(0,2)

def client_fragment(request, id):
    client = get_object_or_404(Client, id=id)
    return render_to_response("client_fragment.html", {'client': client},
                              context_instance=RequestContext(request))

def list_fragment(request):
    clients = Client.objects.all()
    sort = request.GET.get("sort","study_group")
    clients = clients.order_by(sort)
    group = request.GET.get("group",4)
    if int(group) != 4:
		clients = clients.filter(study_group__exact=int(group))
    return render_to_response("list_fragment.html", {'clients': clients},
                              context_instance=RequestContext(request))

def edit_client(request, id):
    client = get_object_or_404(Client, id=id)
    form = None
    if request.method == "GET":
        form = ClientForm(instance=client)

    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        for i in form:
			if i.errors:
				print i,i.errors
        if form.is_valid():
            form.save()
            return HttpResponse('')
    c = {
        "form": form,
    }
    return render_to_response("edit_client.html", c,
                              context_instance=RequestContext(request))
    
def add_message(request, id_number):
    try:
        if request.method == 'POST':
            text = request.POST['text']
            nurse = get_object_or_default(Nurse, None, user=request.user)
            if nurse:
                sender = 'Nurse'
            else:
                sender = 'System'
            client = get_object_or_404(Client, id=id_number)
            message_client(client, nurse, sender, text) # task.message_client
            return HttpResponse('')
    except Exception as e:
        print >> sys.stderr, e

def add_call(request, id_number):
    if request.method == "POST":
        nurse = get_object_or_default(Nurse, None, user=request.user)
        client = get_object_or_404(Client, id=id_number)
        content = request.POST['text']
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
    
def delivery(request, id):
	client = get_object_or_404(Client, id=id)
	client.pregnancy_status = "Post-Partum"
	client.save()
	return HttpResponse('')

def csv_helper(**filter_kwargs):
    field_list = ['id', 'last_name', 'first_name', 'phone_number', 'birth_date',
         'pregnancy_status', 'due_date', 'years_of_education']
    clients = Client.objects.all().order_by('id').filter(**filter_kwargs).values(*field_list)
    field_list += ['conditions']
    response = HttpResponse(';'.join(field_list) + "\n", mimetype="text/csv")
    conditions = dict([(cond.pk, cond.name) for cond in Condition.objects.all()])
    writer = DictWriter(response, field_list, delimiter=";")
    for client in clients:
        client_obj = Client.objects.get(id=client['id'])
        client['conditions'] = [conditions[x.pk] for x in client_obj.conditions.all()]
        writer.writerow(client)
    response['Content-Disposition'] = 'attachment; filename=clients.csv'
    return response

def csv(request):
    return csv_helper()

def clientcsv(request, id_number):
    return csv_helper(id=id_number)

def message_csv(request, id_number):
    client = get_object_or_404(Client, id=id_number)
    field_list = ['date', 'from', 'message']
    response = HttpResponse(';'.join(field_list) + "\n", mimetype="text/csv")
    writer = DictWriter(response, field_list, delimiter=";")
    for x in Interaction.objects.filter(client_id=client):
        row = {
            'date': x.date,
            'from': 'Phone Log' if x.hasphoneattr() else x.message.sent_by,
            'message': x.content,
        }
        writer.writerow(row)
    response['Content-Disposition'] = 'attachment; filename=messages.csv'
    return response
