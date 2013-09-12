from datetime import datetime, date, timedelta
from hashlib import sha256 as sha
import math,sys

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
		ordering = ['-pk']
		
	
	groups = models.ManyToManyField("MessageGroup")

	priority = models.IntegerField(default=0)

	message = models.TextField(max_length=200)

	send_base = models.ForeignKey("MessageBase", blank=True, null=True)

	send_offset = models.IntegerField(default=0)

	#lookup message by key
	key = models.CharField(max_length=25, blank=True, null=True)

	#linked list of next messages
	next_message = models.ForeignKey("self", blank=True, null=True, related_name="previous_message")
	
	note = models.CharField(max_length=250,blank=True)
	
		
	def __unicode__(self):
		out = '{send_offset} from {send_base}'.format(
				pri=self.priority,
				msg=self.message,
				send_base= self.send_base if self.send_base else None,
				send_offset=self.send_offset,
			)
		
		if self.pk:
			out = self.list_groups()+out
		return out
		
	def copy(self):
		"""Deep copy of message"""
		return AutomatedMessage(priority=self.priority,message=self.message,send_base=self.send_base,
		send_offset=self.send_offset,key=self.key,next_message=self.next_message,note=self.note)
		
	def list_groups(self):
		"""return string list of all groups"""
		if self.pk:
			return "{groups} ".format(groups=','.join([str(g) for g in self.groups.all()]))
		
	def send(self,client,previous=False):
		"""
		Send message if it is not a second message
		or if this is a recurisve call for a second message
		"""
		import patients.tasks as _tasks

		if not self.previous_message.exists() or previous:
			#print >> sys.stderr, "Sending AutomatedMessage: ",self
			_tasks.message_client(client,None,"System",self.message)
			if self.next_message:
				self.next_message.send(client,previous=True)
	

class MessageBase(models.Model):
	"""Set initial message send base"""
	name = models.CharField(max_length=100)
	display = models.CharField(max_length=100, blank=True)

	def __unicode__(self):
		#if self.display:
			#return self.display.title()
		return self.name.title()

class MessageGroup(models.Model):
	""" Super class for Message Groups """
	name = models.CharField(max_length=100)
	display = models.CharField(max_length=100, blank=True)

	def __unicode__(self):
		#if self.display:
			#return self.display.title()
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

