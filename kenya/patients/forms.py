from django.forms import IntegerField, CharField, DateField, Form, ModelForm, ChoiceField
from django.forms.widgets import CheckboxSelectMultiple

import patients.models as _patients

class AddClientForm(ModelForm):
	class Meta:
		model = _patients.Client
		fields = ('id', 'first_name', 'last_name', 'nickname','phone_number','birth_date', 'pregnancy_status', 'condition', 'due_date',
		 'relationship_status', 'living_children', 'previous_pregnacies','years_of_education','send_day','send_time','next_visit', 
		 'phone_network' , 'partner_first_name', 'partner_last_name', 'pri_contact_name', 'pri_contact_number', 'sec_contact_name', 
		 'sec_contact_number', 'study_group','language','anc_num')

	id = IntegerField(required=False)
	
	def clean_first_name(self):
		return self.cleaned_data['first_name'].capitalize()
	def clean_last_name(self):
		return self.cleaned_data['last_name'].capitalize()
	def clean_nickname(self):
		return self.cleaned_data['nickname'].capitalize()


class ClientForm(ModelForm):
	
    class Meta:
        model = _patients.Client
        fields = ('nickname','birth_date', 'pregnancy_status', 'condition', 'due_date','next_visit')
		

class MessageForm(ModelForm):
	class Meta:
		model = _patients.Message

class EndPregnacyForm(ModelForm):
	class Meta:
		model = _patients.PregnancyEvent
		fields = ('date','location','outcome')

class VisitForm(Form):
	date = DateField()
	comments = CharField(max_length=100,initial="Planned Visit.")
	next_visit = DateField()
    
