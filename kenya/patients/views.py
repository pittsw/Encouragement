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

from patients.forms import AddClientForm, ClientForm, MessageForm, VisitForm, EndPregnacyForm
from patients.models import *
from backend.models import *
import patients.tasks as tasks

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
	nurse = get_object_or_default(Nurse, None, user=request.user)
	if not nurse==None:
		client.pending = 0
		client.save()
	message_template = "message_frag.html"
	if request.GET.get('mode','conversation') == 'list':
		message_template = "message_listmode.html"
	messages = Interaction.objects.filter(client_id=client)
	return render_to_response(message_template, {"client": str(client), "messages":messages}, context_instance=RequestContext(request))

def client(request):
	if request.method == "GET":
		if "id" in request.GET:
			client = Client.objects.get(id=request.GET["id"])
			isList = request.GET.get('list')
			return render_to_response("display_client_fragment.html",
				{"client":client,
				"list":isList,
				"notes": Note.objects.filter(client_id=client),
				"history": Visit.objects.filter(client_id=client),
				"client_fragment": render_to_string("client_fragment.html", {"client":client}, context_instance=RequestContext(request)),
				"visit_form": render_to_string("visit_form.html", 
					{"form": VisitForm(initial={"next_visit":client.next_visit,'date':date.today()}),'client':client}, 
					context_instance=RequestContext(request)),
				"end_pregnacy_form":EndPregnacyForm(prefix="end",initial={'date':date.today(),'outcome':'live_birth','location':'clinic'}),
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
            client.next_visit = form.cleaned_data['next_visit']
            client.save()
            return HttpResponse('')
    return render_to_response('visit_form.html', {'form': form,'client':client})
    
def visit_history(request):
	missed = Client.objects.filter(next_visit__lt=date.today())
	today = Client.objects.filter(next_visit=date.today())
	future = Client.objects.filter(next_visit__gt=date.today(),next_visit__lte=date.today()+timedelta(days=2))
	if request.method == "GET":
		return render_to_response('visit_history.html',{'missed':missed,'today':today,'future':future},RequestContext(request))
	#Process Post POST
	updates = {}
	messages = {'missed':'Patient arrived late','today':'Planned Visit','future':'Patient arrived early'}
	#get clients to update from checkboxs
	for name,value in request.POST.iteritems():
		try:
			box,when,client_id = name.split('_')
			if(box=='ck' and value=='on'):
				try:
					updates[when].append(client_id)
				except KeyError, e:
					updates[when] = [client_id]
		except ValueError:
			pass
	out = ""
	#Todo: Error Checking
	for when,client_ids in updates.iteritems():
		for client_id in client_ids:
			new_date = request.POST['date_%s'%(client_id)]
			out += '(%s) %s:%s<br/>\n'%(client_id,new_date,messages[when])
			#Make this actually change the client
			tmp_client = Client.objects.get(id=client_id)
			tmp_client.next_visit = new_date
			tmp_client.save()
			#create visit event
			visit = Visit(client_id=tmp_client,comments=messages[when],date=date.today())
			visit.save()
	return HttpResponse(out)

def delete_visit(request, pk):
    if request.method == "POST":
		visit = get_object_or_404(Visit, pk=pk)
		visit.delete()
		return HttpResponse('')
	

def add_client(request):
    form = None
    c = {}
    if request.method == "GET":
        next_month = (date.today() + timedelta(30)).strftime("%Y-%m-")
        due_date = (date.today() + timedelta(180)).strftime("%Y-%m-")
        form = AddClientForm(initial={"birth_date":"1990-","due_date":due_date,"next_visit":next_month,"condition":"1",
        "previous_pregnacies":"1","living_children":"0","years_of_education":"1","phone_number":"254","pri_contact_number":"254",
        "sec_contact_number":"254",})
    elif request.method == "POST":
		form = AddClientForm(request.POST)
		if form.is_valid():
			id = form.cleaned_data['id']
			client = form.save(commit=False)
			client.id = id
			client.save()
			#Send initial message for language
			#Exclude control group
			message = AutomatedMessage.objects.filter(send_base__name__exact="signup").filter(send_offset__exact=-1)\
			.filter(groups=client.language)
			if message.count() > 0:
				message[0].send(client)
			
			return HttpResponse(str(client.id)) #return new client id
    return render_to_response("add_client.html", {'form': form},
                              context_instance=RequestContext(request))

def client_fragment(request, id):
    client = get_object_or_404(Client, id=id)
    return render_to_response("client_fragment.html", {'client': client},
                              context_instance=RequestContext(request))

def list_fragment(request):
	clients = Client.objects.all()
	sort = request.GET.get("sort","study_group")
	clients = clients.order_by(sort)
	group,status = request.GET.get("group",',').split(',')
	group = get_object_or_default(StudyGroup,None,name=group) if group else None
	if group:
		clients = clients.filter(study_group=group)
	clients = clients.filter(pregnancy_status__contains=status)
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
    try:
        if request.method == 'POST':
            text = request.POST['text'].strip()
            nurse = get_object_or_default(Nurse, None, user=request.user)
            if nurse:
                sender = 'Nurse'
            else:
                sender = 'System'
            client = get_object_or_404(Client, id=id_number)
            tasks.message_client(client, nurse, sender, text) # task.message_client
            return HttpResponse('')
    except Exception as e:
        print >> sys.stderr, "Add Message",e

def add_call(request, id_number):
    if request.method == "POST":
        nurse = get_object_or_default(Nurse, None, user=request.user)
        client = get_object_or_404(Client, id=id_number)
        content = request.POST['text']
        duration = request.POST['duration']
        reason = request.POST.get('reason','other')
        initiated = request.POST['initiated']
        try:
            duration = int(duration)
        except ValueError:
            duration = 0
        PhoneCall(
            user_id=nurse,
            client_id=client,
            content=content,
            duration=duration,
            reason=reason,
            caller=initiated,
        ).save()
    return HttpResponse('')
    
def message_prompted(request,id_number):
	message = get_object_or_404(Message,id=id_number)
	message.prompted = True if request.GET.get('prompted',"true").lower() == "true" else False 
	message.save()
	return HttpResponse('')

def pregnacy(request, id):
	form = EndPregnacyForm(prefix="end",initial={'date':date.today()})
	if request.method == "POST":
		client = get_object_or_404(Client, id=id)
		form = EndPregnacyForm(request.POST,prefix="end")
		if form.is_valid():
			#print "Vaild: %s, %s, %s"%(form.cleaned_data['date'],form.cleaned_data['location'],form.cleaned_data['outcome'])
			pregnacy_event = form.save(commit=False)
			pregnacy_event.client = client
			pregnacy_event.save()
			#update client pregnacy_status
			if pregnacy_event.outcome == "live_birth":
				client.pregnancy_status = "Post-Partum"
			elif pregnacy_event.outcome == "miscarriage":
				client.pregnancy_status = "Stopped"
			client.save()
			#create a visit record
			visit = Visit(client_id=client,comments=pregnacy_event.message(),date=date.today())
			visit.save()
			return HttpResponse('')
	return HttpResponse(form.as_table())

def test(request):
	pregnant,post,visit = [],[],[]
	day = datetime.now()
	if request.method == "POST":
		if request.POST['date']:
			day = datetime.strptime(request.POST['date'],"%Y-%m-%d")
			day += timedelta(hours=int(request.POST['hour']))
			pregnant,post,visit = tasks.get_all_scheduled(day)
		else:
			pregnant,post,visit = tasks.send_all_scheduled()
	return render_to_response("test.html", {'pregnant':pregnant,'post':post,'visit':visit,
	'date':day.strftime("%Y-%m-%d")}, context_instance=RequestContext(request))
	
	
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
