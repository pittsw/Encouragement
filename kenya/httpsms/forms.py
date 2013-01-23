from django import forms
from patients.models  import Client, AutomatedMessage
import time,md5

class SendForm(forms.Form):
	sender_number = forms.CharField(max_length=16)
	content = forms.CharField(widget=forms.widgets.Textarea)
	
	@classmethod
	def msgID(cls):
		return md5.new(str(time.gmtime())).hexdigest()
		
class SystemForm(forms.Form):
	client = forms.ModelChoiceField(queryset=Client.objects.filter(phone_number__gt=""))
	message = forms.ModelChoiceField(queryset=AutomatedMessage.objects.all())
