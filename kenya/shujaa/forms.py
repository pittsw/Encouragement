from django.forms import IntegerField, CharField, DateField, Form, ModelForm, ChoiceField, Textarea
from patients.models import Client

class TestMessage(Form):
	to = CharField(max_length=15)
	message = CharField(widget=Textarea,max_length=160)
	network = ChoiceField(Client.NETWORK_CHOICES)
