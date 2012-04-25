from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
	name = models.CharField(max_length=50)
	def __unicode__(self):
		return self.name

class Client(models.Model):
	id = models.IntegerField(primary_key = True)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	phone_number = models.IntegerField()
	birth_date = models.DateField()
	location = models.ForeignKey(Location)
	BABY_CHOICES = (
		('Born', 'Born'),
		('Unborn', 'Unborn'),
	)
	baby_status = models.CharField(max_length = 6, choices=BABY_CHOICES)
	due_date = models.DateField()
	def __unicode__(self):
		return self.first_name + ' ' + self.last_name

class Nurse(models.Model):
	id = models.IntegerField(primary_key = True)
	user = models.OneToOneField(User)
	location = models.ForeignKey(Location)
	def __unicode__(self):
		return self.user.first_name + ' ' + self.user.last_name

class Message(models.Model):
	SENDER_CHOICES = (
		('Client', 'Client'),
		('Nurse', 'Nurse'),
		('System', 'System'),
	)
	client_id = models.ForeignKey(Client)
	user_id = models.ForeignKey(Nurse)
	sent_by = models.CharField(max_length = 6, choices=SENDER_CHOICES)
	content = models.CharField(max_length=500)
	priority = models.IntegerField()
	date = models.DateTimeField(auto_now_add = True)
	def __unicode__(self):
		return self.content

