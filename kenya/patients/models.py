from datetime import datetime, date, timedelta
from hashlib import sha256 as sha
import math

from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import pytz

class Location(models.Model):

    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Client(models.Model):

    class Meta:
        ordering = ['-urgent', '-pending', '-last_msg']
        
    STATUS_CHOICES = (
        ('Pregnant', 'Pregnant'),
        ('Post-Partum', 'Post-Partum'),
        ('Failed Pregnancy', 'Failed Pregnancy'),
    )
    
    primary_key = models.AutoField(primary_key=True)
    
    id = models.IntegerField(unique=True)

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    phone_number = models.CharField(max_length=50, blank=True, editable=False)

    birth_date = models.DateField()

    location = models.ForeignKey(Location)

    pregnancy_status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    due_date = models.DateField()

    years_of_education = models.IntegerField()

    conditions = models.ManyToManyField('Condition')

    urgent = models.BooleanField(editable=False, default=False)

    pending = models.IntegerField(editable=False, default=0)

    last_msg = models.DateField(blank=True, null=True, editable=False)

    sent_messages = models.ManyToManyField('AutomatedMessage', blank=True, editable=False)

    def clean(self):
        if None in [self.birth_date, self.due_date, self.years_of_education]:
            return
        low_age = 10
        high_age = 100
        one_year = timedelta(days=365)
        today = date.today()
        errors = []
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
        return self.first_name + ' ' + self.last_name

    def last_message(self):
        message = Message.objects.filter(client_id=self, sent_by='Client')
        if message.count() < 1:
            return "No messages yet"
        else:
            return message[0]

    def generate_key(self):
        key_length = 7.0
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
        self.pending = len(messages.filter(read=False))
        self.urgent = (datetime.now(pytz.utc) - self.last_msg) > settings.URGENT
        self.save()


class Nurse(models.Model):

    id = models.IntegerField(primary_key=True)

    user = models.OneToOneField(User)

    location = models.ForeignKey(Location)
    
    def __unicode__(self):
        return self.user.first_name

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

    read = models.BooleanField(default=False, editable=False)

class SMSSyncOutgoing(models.Model):

    target = models.CharField(max_length=50)

    content = models.CharField(max_length=1000)

    def __unicode__(self):
        return '"{cont}" >> {tar}'.format(cont=self.content, tar=self.target)


class Condition(models.Model):
    """Choo choo!

    """

    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class AutomatedMessage(models.Model):
    """These are the individual automated messages that are sent out
    twice a week.

    Fields:
        condition - which condition this AutomatedMessage is a part of
        priority - the priority of this message -- higher numbers better
        message - the contents of the message
        start_week - add this many weeks to the date of birth to
                     calculate the earliest this message can be sent
        end_week - add this many weeks to the date of birth to
                   calculate the latest this message can be sent

    """

    class Meta:
        ordering = ['-priority']

    condition = models.ForeignKey(Condition)

    priority = models.IntegerField(default=0)

    message = models.CharField(max_length=144)

    start_week = models.IntegerField()

    end_week = models.IntegerField()

    repeats = models.BooleanField(default=False)

    def __unicode__(self):
        return '{con} ({pri}): "{msg}", {stw} to {end}'.format(
            con=self.condition,
            pri=self.priority,
            msg=self.message,
            stw=self.start_week,
            end=self.end_week,
        )


class Note(models.Model):
    class Meta:
        ordering = ['-date']
        
    client_id = models.ForeignKey(Client)
    
    author_id = models.ForeignKey(Nurse)
    
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
