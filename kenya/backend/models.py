from datetime import datetime, date, timedelta
from hashlib import sha256 as sha
import math

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models

class AutomatedMessage(models.Model):
    """These are the individual automated messages that are sent out
    twice a week.

    Fields:
        condition: which condition this AutomatedMessage is a part of
        priority: the priority of this message -- the higher the more important and sent first
        message: the contents of the message
		send_base: The place to start counting sending from (signup, estimated delivery, anytime)
		send_offset: The offset number from send_base to send.  For anytime messages this is the sequance number.
    """
    
    SEND_BASE_CHOICES = ( ('signup','Sign Up'),
    				('edd','Delivery Date'),
    				('anytime','Anytime'),
    				('named','Named'),
    				)
    

    class Meta:
        ordering = ['-priority']

    condition = models.ForeignKey('Condition')

    priority = models.IntegerField(default=0)

    message = models.TextField(max_length=200)

    send_base = models.CharField(max_length=10, choices=SEND_BASE_CHOICES, default="edd")
    
    send_offset = models.IntegerField(default=0)
    
    name = models.CharField(max_length=25, blank=True)
    
    def __unicode__(self):
        return '{con} ({pri}): "{msg}", send {send_offset} from {send_base}'.format(
            con=self.condition,
            pri=self.priority,
            msg=self.message,
            send_base=self.send_base,
            send_offset=self.send_offset,
        )

class Condition(models.Model):
    """Used to determine which automated messages a patient gets
    """
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class Email(models.Model):
	
	subject = models.CharField(max_length=100)
	
	content = models.TextField(max_length=600)
	
	key = models.CharField(max_length=100)
	
	def __unicode__(self):
		return "%s | %s"%(self.key,self.subject)
		
class AutoTask(models.Model):
	
	timestamp = models.DateTimeField(auto_now=True)
	function = models.CharField(max_length=20)
	
	def __unicode__(self):
		return "'%s':\t%s"%(self.function, self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
