from patients.models import Client, Message
from django.forms import ModelForm

class ClientForm(ModelForm):
    class Meta:
        model = Client
        
class MessageForm(ModelForm):
    class Meta:
        model = Message
        

    