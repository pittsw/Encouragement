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
					('edd','Estimated Delivery Date'),
					('visit','Visit'),
					('dd','Delivery Date'),
					)


	class Meta:
		ordering = ['-priority']
		
	
	groups = models.ManyToManyField("MessageGroup")

	priority = models.IntegerField(default=0)

	message = models.TextField(max_length=200)

	send_base = models.ForeignKey("MessageBase", blank=True, null=True)

	send_offset = models.IntegerField(default=0)

	#lookup message by key
	key = models.CharField(max_length=25, blank=True, null=True)

	#linked list of next messages
	next_message = models.ForeignKey("self", blank=True, null=True)
	
	note = models.CharField(max_length=250)
		
	def __unicode__(self):
		return 'Groups: ({groups}) {send_offset} from {send_base}<br/>\n <b>"{msg}"</b>'.format(
			groups=','.join([str(g) for g in self.groups.all()]),
			pri=self.priority,
			msg=self.message,
			send_base= self.send_base if self.send_base else None,
			send_offset=self.send_offset,
		)

class MessageBase(models.Model):
	"""Set initial message send base"""
	name = models.CharField(max_length=100)
	display = models.CharField(max_length=100, blank=True)

	def __unicode__(self):
		if self.display:
			return self.display.title()
		return self.name.title()

class MessageGroup(models.Model):
	""" Super class for Message Groups """
	name = models.CharField(max_length=100)
	display = models.CharField(max_length=100, blank=True)

	def __unicode__(self):
		if self.display:
			return self.display.title()
		return self.name.title()

class Condition(MessageGroup):
	"""Used to determine which automated messages a patient gets """
		
class StudyGroup(MessageGroup):
	""" Control group for study.  Primary sort key for messages"""

class LanguageGroup(MessageGroup):
	"""Mark the language of the message"""

class Email(models.Model):
	
	subject = models.CharField(max_length=100)
	
	content = models.TextField(max_length=600)
	
	key = models.CharField(max_length=100)
	
	def __unicode__(self):
		return "%s | %s"%(self.key,self.subject)
		
class AutoTask(models.Model):
	
	timestamp = models.DateTimeField(auto_now=True)
	function = models.CharField(max_length=20)
	data = models.CharField(max_length=1000, blank=True)
	
	def __unicode__(self):
		return "'%s':\t%s"%(self.function, self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))
