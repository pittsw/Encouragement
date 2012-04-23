from django.shortcuts import render_to_response
from patients.models import Client, Message, Location, Nurse
from django.views.decorators.csrf import csrf_exempt

def index(request):
	return render_to_response("index.html")

def client(request, id_number):
	try:
		client = Client.objects.get(id=id_number)
		messages = Message.objects.filter(client_id=client)
		return render_to_response("display.html", {"client":client, "messages":messages})
	except Page.DoesNotExist:
		return render_to_response("form.html")
	
def list_clients(request):
	clients = Client.objects.all()
	return render_to_response("list.html", {"clients":clients})

@csrf_exempt
def add(request):
	if request.POST:
		id_number = request.POST["id"]
		fname = request.POST["fname"]
		lname = request.POST["lname"]
		pnumber = request.POST["phone"]
		bday = request.POST["bday"]
		locale = Location.objects.get(name=request.POST["location"])
		person = Client(id = id_number, first_name = fname,	last_name = lname, phone_number = pnumber, birth_date = bday, location = locale)
		person.save()
		locales = Location.objects.all()
		return render_to_response("form.html", {"locations":locales})
	else:
		locales = Location.objects.all()
		return render_to_response("form.html", {"locations":locales})
		
@csrf_exempt
def add_message(request):
	if request.POST:
		client_id = request.POST["cid"]
		user_id = request.POST["uid"]
		sent_by = request.POST["sentby"]
		content = request.POST["content"]
		priority = request.POST["priority"]
		date = request.POST["date"]
		m = Message(client_id=Client.objects.get(id=client_id), user_id=Nurse.objects.get(id=user_id), sent_by = sent_by, content = content, priority = priority, date = date)
		m.save()
		people = Client.objects.all()
		nurses = Nurse.objects.all()
		return render_to_response("message.html", {"people":people, "nurses":nurses, "choice":Message.SENDER_CHOICES})
	else:
		people = Client.objects.all()
		nurses = Nurse.objects.all()
		return render_to_response("message.html", {"people":people, "nurses":nurses, "choice":Message.SENDER_CHOICES})

	

	