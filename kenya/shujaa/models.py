from django.db import models

import patients.models as patients

# Create your models here.from django.db import models

class ShujaaMsg(models.Model):
	
	client_number = models.CharField(max_length=15)
	
	message = models.CharField(max_length=300)
	
	network = models.CharField(max_length=50, choices=patients.Client.NETWORK_CHOICES,default="safaricom")
	
	response = models.CharField(max_length=40)
	
	def __unicode__(self):
		return "Shujaa: {} to {}".format(self.message,self.client_number)
