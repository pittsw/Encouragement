from datetime import datetime, date, timedelta
from hashlib import sha256 as sha
import math

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
import pytz

import backend.models as _backend

class Client(models.Model):
		
	STATUS_CHOICES = (
		('Pregnant', 'Pregnant'),
		('Post-Partum', 'Post-Partum'),
		('Stopped', 'Left Study'),
		('Finished', 'Finished Study'),
	)

	RELATIONSHIP_CHOICES = (
		('Single','Single'),
		('Parner','Parner'),
		('Married','Married'),
    )
    
	DAY_CHOICES = (
		(0,'Monday'),
		(1,'Tuesday'),
		(2,'Wednesday'),
		(3,'Thursday'),
		(4,'Friday'),
		(5,'Saturday'),
		(6,'Sunday'),
	)
	
	TIME_CHOICES = (
		(8,"Morning"),
		(13,"Afternoon"),
		(19,"Evening"),
	)
	
	NETWORK_CHOICES = (
		("safaricom","Safaricom"),
		("airtelkenya","Airtel"),
	)
	
	primary_key = models.AutoField(primary_key=True)

	id = models.PositiveIntegerField(unique=True)
	
	anc_num = models.PositiveIntegerField(blank=True,null=True)

	first_name = models.CharField(max_length=50)

	last_name = models.CharField(max_length=50)

	nickname = models.CharField(max_length=50)

	birth_date = models.DateField()

	relationship_status = models.CharField(max_length=25, choices=RELATIONSHIP_CHOICES, default="Married")

	partner_first_name = models.CharField(max_length=50, blank=True)

	partner_last_name = models.CharField(max_length=50, blank=True)

	pri_contact_name = models.CharField(max_length=50)
	 
	pri_contact_number = models.CharField(max_length=50)
	 
	sec_contact_name = models.CharField(max_length=50, blank=True)
	 
	sec_contact_number = models.CharField(max_length=50, blank=True)

	pregnancy_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pregnant")

	due_date = models.DateField()

	years_of_education = models.IntegerField()

	living_children = models.IntegerField()

	previous_pregnacies = models.IntegerField()

	condition = models.ForeignKey(_backend.Condition)
	
	language = models.ForeignKey(_backend.LanguageGroup,default="English")

	next_visit = models.DateField(blank=True, null=True)

	study_group = models.ForeignKey(_backend.StudyGroup)

	#Send Message Attributes
	phone_number = models.CharField(max_length=50, blank=True, unique=True)

	phone_network = models.CharField(max_length=50, choices=NETWORK_CHOICES,default="safaricom")

	send_day = models.IntegerField(choices=DAY_CHOICES, default=3)

	send_time = models.IntegerField(choices=TIME_CHOICES, default=13)

	#Attributes to be edited by system only
	urgent = models.BooleanField(default=False)
	
	repeat_msg = models.IntegerField(editable=False,default=0)

	pending = models.IntegerField(editable=False, default=0)

	last_msg_client = models.DateField(blank=True, null=True, editable=False)
	
	last_msg_system = models.DateField(blank=True, null=True, editable=False)
	
	validated = models.BooleanField(default=False)

	signup_date = models.DateField(editable=False, auto_now_add=True)

	def clean(self):
		if None in [self.birth_date, self.due_date, self.years_of_education]:
			return
		low_age = 10
		high_age = 100
		one_year = timedelta(days=365)
		today = date.today()
		errors = []
		if self.id > 1000:
			errors.append('Study ID must be less than 1000')
		if self.pregnancy_status == 'Pregnant' and self.due_date < today:
			errors.append('Client is pregnant but expected delivery '+\
				'date is in the past')
		if self.pregnancy_status == 'Post-Partum' and self.due_date > today:
			errors.append('Client has given birth by date of birth of '+\
				'the child is in the future.')
		if today.year - low_age < self.birth_date.year:
			errors.append('Client is under {low_age} years old'.format(
				low_age=low_age))
		if today.year - high_age > self.birth_date.year:
			errors.append('Client is over {high_age} years old'.format(
				high_age=high_age))
		if (self.due_date - today) > one_year:
			errors.append('Expected due date is over a year away')
		if (today.year - self.birth_date.year) <= self.years_of_education:
			errors.append("Client has been in school longer than she's been "
				"alive")
		if errors:
			raise ValidationError(errors)

	def details(self):
		return "Phone Number: %s -- %s %s (#%03i) -- Study Group: %s"%(self.phone_number,self.first_name,self.last_name,self.id,self.study_group)
		
	def __unicode__(self):
		return  "(#%03s) %s %s"%(self.id,self.first_name,self.last_name)
		
	def __str__(self):
		return "%s %s"%(self.first_name,self.last_name)

	def last_message(self):
		message = Message.objects.filter(client_id=self, sent_by='Client')
		if message.count() < 1:
			return "No messages yet"
		else:
			return message[0]

	def generate_key(self):
		key_length = 5.0
		chars = "ABCDEFGHIJKLMNOP"
		string = (sha(str(self.id) + self.first_name + self.last_name)
			.hexdigest())
		step = int(math.ceil(len(string) / key_length))
		return ''.join([chars[int(x, 16)] for x in string[::step]])

class PregnancyEvent(models.Model):
	
	OUTCOME_CHOICES = (
		('live_birth','Live Birth'),
		('miscarriage','Miscarriage'),
	)
	
	LOCATION_CHOICES = (
		('home','Home'),
		('clinic','Clinc'),
		('hosptital','Hospital'),
	)
	
	date = models.DateField()
	
	outcome = models.CharField(max_length=20, choices=OUTCOME_CHOICES,default="live_birth")
	
	location = models.CharField(max_length=20, choices=LOCATION_CHOICES,default="home")
	
	client = models.OneToOneField(Client,null=True,blank=True)
	
	def message(self):
		if self.outcome=='live_birth':
			return "Live birth at {}".format(self.location)
		return "Miscarriage at {}".format(self.location)
	
	def __unicode__(self):
		return "(%s) %s (%s)"%(self.date,self.client,self.outcome)

class Nurse(models.Model):

	id = models.IntegerField(primary_key=True)

	user = models.OneToOneField(User)

	def __unicode__(self):
		return self.user.first_name
		# consider making this first AND last names.

class Interaction(models.Model):
	class Meta:
		ordering = ['-date']
		
	date = models.DateTimeField(auto_now_add=True)

	user_id = models.ForeignKey(Nurse, blank=True, null=True)

	client_id = models.ForeignKey(Client)

	content = models.CharField(max_length=1000)

	def hasphoneattr(self):
		return hasattr(self, 'phonecall')

	def __unicode__(self):
		return self.content
		
	def getClassName(self):
		return self.__class__.__name__

class Message(Interaction):
	SENDER_CHOICES = (
		('Client', 'Client'),
		('Nurse', 'Nurse'),
		('System', 'System'),
	)

	sent_by = models.CharField(max_length=6, choices=SENDER_CHOICES)

	prompted = models.BooleanField(default=True)

class PhoneCall(Interaction):

	REASON_CHOICES = ( 
		("visit","Missed ANC Visit"),
		("sms","No SMS Response"),
		("other","other"),
	)

	CALLER_CHOICES = (
		('nurse','Nurse'),
		('client','Client'),
	)

	duration = models.IntegerField(default=0)
	
	reason = models.CharField(max_length=10, choices=REASON_CHOICES, default="other")
	
	caller = models.CharField(max_length=10, choices=CALLER_CHOICES, default="nurse")

class Note(models.Model):
    class Meta:
        ordering = ['-date']
        
    client_id = models.ForeignKey(Client)
    
    author_id = models.ForeignKey(Nurse, blank=True, null=True)
    
    content = models.CharField(max_length=500)
    
    date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.content

class Visit(models.Model):
	class Meta:
		ordering = ['-date']
		
	client_id = models.ForeignKey(Client)

	comments = models.CharField(max_length=100)

	date = models.DateField()
	
	scheduled_date = models.DateField(null=True,blank=True)

	def __unicode__(self):
		return self.comments
		
#class Reports(models.Model):
	
	#date = models.DateField()
