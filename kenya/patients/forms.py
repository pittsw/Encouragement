from django.forms import IntegerField, CharField, DateField, Form, ModelForm, ChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from patients.models import Client, Message, Visit
import random

class AddClientForm(ModelForm):
	class Meta:
		model = Client
		fields = ('id', 'first_name', 'last_name', 'nickname','phone_number','birth_date', 'pregnancy_status', 'conditions', 'due_date', 'relationship_status', 'partner_name', \
			'living_children', 'previous_pregnacies','years_of_education','send_day','send_time','next_visit')
		widgets = {
			'conditions': CheckboxSelectMultiple,
		}

	id = IntegerField(required=False)


class ClientForm(ModelForm):
	
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'nickname','birth_date', 'pregnancy_status', 'conditions', 'due_date', 'years_of_education',\
        'send_day','send_time','next_visit')
        widgets = {
            'conditions': CheckboxSelectMultiple,
        }
		

class MessageForm(ModelForm):
	class Meta:
		model = Message


class VisitForm(Form):
	date = DateField()
	comments = CharField(max_length=100)
	next_visit = DateField()
    
