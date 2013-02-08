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

class Client(models.Model):

	class Meta:
		ordering = ['-urgent', '-pending', '-last_msg']
		
	STATUS_CHOICES = (
		('Pregnant', 'Pregnant'),
		('Post-Partum', 'Post-Partum'),
		('Failed Pregnancy', 'Failed Pregnancy'),
		('Stopped', 'Left Study'),
	)

	RELATIONSHIP_CHOICES = (
		('Single','Single'),
		('Parner','Parner'),
		('Married','Married'),
    )
    
	DAY_CHOICES = (
		(1,'Monday'),
		(2,'Tuesday'),
		(3,'Wednesday'),
		(4,'Thursday'),
		(5,'Friday'),
		(6,'Saturday'),
		(0,'Sunday'),
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
	
	STUDY_GROUP_CHOICES = (
		("two-way","Two Way"),
		("one-way","One Way"),
		("control","Control"),
	)
	
	LANGUAGE_CHOICES = (
		("English","English"),
		("Kiswahili","Kiswahili"),
	)

	primary_key = models.AutoField(primary_key=True)

	id = models.PositiveIntegerField(unique=True)

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

	conditions = models.ManyToManyField('Condition', blank=True)
	
	language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default="English")

	next_visit = models.DateField(blank=True, null=True)

	study_group = models.CharField(max_length=20, choices=STUDY_GROUP_CHOICES)

	#Send Message Attributes
	phone_number = models.CharField(max_length=50, blank=True, unique=True)

	phone_network = models.CharField(max_length=500, choices=NETWORK_CHOICES,default="safaricom")

	send_day = models.IntegerField(choices=DAY_CHOICES, default=3)

	send_time = models.IntegerField(choices=TIME_CHOICES, default=13)

	#Attributes to be edited by system only
	urgent = models.BooleanField(editable=False, default=False)

	pending = models.IntegerField(editable=False, default=0)

	last_msg = models.DateField(blank=True, null=True, editable=False)

	sent_messages = models.ManyToManyField('AutomatedMessage', blank=True, editable=False)
	
	validated = models.BooleanField(editable=False,default=False)

	signup_date = models.DateField(editable=False, auto_now_add=True)

	def clean(self):
		if None in [self.birth_date, self.due_date, self.years_of_education]:
			return
		low_age = 10
		high_age = 100
		one_year = timedelta(days=365)
		today = date.today()
		errors = []
		if self.id > 99999:
			errors.append('Study ID must be less than 1000')
		if self.pregnancy_status == 'Pregnant' and self.due_date < today:
			errors.append('Client is pregnant but expected delivery '
				'date is in the past')
		if self.pregnancy_status == 'Post-Partum' and self.due_date > today:
			errors.append('Client has given birth by date of birth of '
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

	def __unicode__(self):
		return "Phone Number: %s -- %s %s (#%s) -- Study Group: %s"%(self.phone_number,self.first_name,self.last_name,self.id,self.study_group)
		
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

	def update(self):
		messages = Message.objects.filter(client_id=self,
										  sent_by='Client')
		if len(messages) == 0:
			return

		self.last_msg = messages[0].date
		self.urgent = (datetime.now(pytz.utc) - self.last_msg) > settings.URGENT
		self.save()


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

#add shuja id
class Message(Interaction):
    SENDER_CHOICES = (
        ('Client', 'Client'),
        ('Nurse', 'Nurse'),
        ('System', 'System'),
    )
    
    sent_by = models.CharField(max_length=6, choices=SENDER_CHOICES)

class Condition(models.Model):
    """Used to determine which automated messages a patient gets
    """
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


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

    condition = models.ForeignKey(Condition)

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


class Email(models.Model):
	
	subject = models.CharField(max_length=100)
	
	content = models.TextField(max_length=600)
	
	key = models.CharField(max_length=100)
	
	def __unicode__(self):
		return "%s | %s"%(self.key,self.subject)

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
    
    def __unicode__(self):
        return self.comments
        
class PhoneCall(Interaction):
    duration = models.IntegerField(default=0)


@receiver(post_save, sender=Message, dispatch_uid="pending_update")
def increment_pending(sender, **kwargs):
    instance = kwargs['instance']
    if instance.sent_by == 'Client' and kwargs['created'] and not kwargs['raw']:
        client = instance.client_id
        client.pending = F('pending') + 1
        client.save()
