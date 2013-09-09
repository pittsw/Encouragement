from django import forms
from patients.models  import Client
from backend.models import AutomatedMessage
import time,md5

class SendForm(forms.Form):
	client = forms.ModelChoiceField(queryset=Client.objects.filter(phone_number__gt=""))
	content = forms.CharField(widget=forms.widgets.Textarea)
	
	@classmethod
	def msgID(cls):
		return md5.new(str(time.gmtime())).hexdigest()
		
class SystemForm(forms.Form):
	client = forms.ModelChoiceField(queryset=Client.objects.filter(phone_number__gt=""))
	message = forms.ModelChoiceField(queryset=AutomatedMessage.objects.all())
