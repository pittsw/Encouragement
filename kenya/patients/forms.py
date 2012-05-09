from django.forms import IntegerField, ModelForm

from patients.models import Client, Message

class AddClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'birth_date', 'location', 'pregnancy_status', 'due_date', 'marital_status', 'years_of_education')

    id = IntegerField()

class ClientForm(ModelForm):
	class Meta:
		model = Client
		
class MessageForm(ModelForm):
	class Meta:
		model = Message
