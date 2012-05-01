from django.forms import ModelForm

from patients.models import Client, Message

class ClientForm(ModelForm):
	class Meta:
		model = Client
        exclude = ('urgent', 'pending', 'last_msg')
		
class MessageForm(ModelForm):
	class Meta:
		model = Message
        exclude = ('read')
