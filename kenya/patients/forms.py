from django.forms import IntegerField, ModelForm
from django.forms.widgets import CheckboxSelectMultiple

from patients.models import Client, Message

class AddClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'birth_date', 'location', 'pregnancy_status', 'conditions', 'due_date', 'years_of_education')
        widgets = {
            'conditions': CheckboxSelectMultiple,
        }

    id = IntegerField(required=False)

class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'birth_date', 'location', 'pregnancy_status', 'conditions', 'due_date', 'years_of_education')
        widgets = {
            'conditions': CheckboxSelectMultiple,
        }
		
class MessageForm(ModelForm):
	class Meta:
		model = Message
