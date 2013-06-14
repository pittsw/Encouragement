from django.forms import IntegerField, CharField, DateField, Form, ModelForm, ChoiceField, Textarea, ValidationError
from patients.models import Client

import re

class TestMessage(Form):
	to = CharField(max_length=15)
	message = CharField(widget=Textarea,max_length=160)
	#network = ChoiceField(Client.NETWORK_CHOICES)
	
	def clean_to(self):
		data = self.cleaned_data['to']
		if not re.match("^254\d*$",data):
			raise ValidationError("Number must start with 254 and be a number")
		return 
	
	def clean_message(self):
		data = self.cleaned_data['message']
		if len(data)>160:
			raise ValidationError("Message To Long")
