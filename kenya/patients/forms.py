from django.forms import IntegerField, CharField, DateField, Form, ModelForm, ChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from patients.models import Client, Message, Visit
import random

class AddClientForm(ModelForm):
	class Meta:
		model = Client
		fields = ('id', 'first_name', 'last_name', 'nickname','birth_date', 'location', 'pregnancy_status', 'father', 'conditions', 'due_date', \
			'years_of_education','message_day','message_time')
		widgets = {
			'conditions': CheckboxSelectMultiple,
		}

	id = IntegerField(required=False)


class ClientForm(ModelForm):
	
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'birth_date', 'location', 'pregnancy_status', 'conditions', 'due_date', 'years_of_education','message_day')
        widgets = {
            'conditions': CheckboxSelectMultiple,
        }
		

class MessageForm(ModelForm):
	class Meta:
		model = Message


class VisitForm(Form):
    comments = CharField(max_length=100)
    date = DateField()
