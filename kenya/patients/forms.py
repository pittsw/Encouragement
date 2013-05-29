from django.forms import IntegerField, CharField, DateField, Form, ModelForm, ChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from patients.models import Client, Message, Visit, PregnaceyEvent
import random

class AddClientForm(ModelForm):
	class Meta:
		model = Client
		fields = ('id', 'first_name', 'last_name', 'nickname','phone_number','birth_date', 'pregnancy_status', 'conditions', 'due_date',
		 'relationship_status', 'living_children', 'previous_pregnacies','years_of_education','send_day','send_time','next_visit', 
		 'phone_network' , 'partner_first_name', 'partner_last_name', 'pri_contact_name', 'pri_contact_number', 'sec_contact_name', 
		 'sec_contact_number', 'study_group','language')
             
		widgets = {
			'conditions': CheckboxSelectMultiple,
		}

	id = IntegerField(required=False)


class ClientForm(ModelForm):
	
    class Meta:
        model = Client
        fields = ('nickname','birth_date', 'pregnancy_status', 'conditions', 'due_date','next_visit')
        widgets = {
            'conditions': CheckboxSelectMultiple,
        }
		

class MessageForm(ModelForm):
	class Meta:
		model = Message

class EndPregnacyForm(ModelForm):
	class Meta:
		model = PregnaceyEvent
		fields = ('date','location','outcome')

class VisitForm(Form):
	date = DateField()
	comments = CharField(max_length=100,initial="Planned Visit.")
	next_visit = DateField()
    
