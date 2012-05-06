from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

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
    
    MARRIAGE_CHOICES = (
        ('Single', 'Single'),
        ('Married', 'Married'),
    )

    id = models.IntegerField(primary_key=True, editable=False)

    first_name = models.CharField(max_length=50)

    last_name = models.CharField(max_length=50)

    phone_number = models.CharField(max_length=50)

    birth_date = models.DateField()

    location = models.ForeignKey(Location)

    pregnancy_status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    due_date = models.DateField()

    marital_status = models.CharField(max_length=20, choices=MARRIAGE_CHOICES)

    years_of_education = models.IntegerField()

    conditions = models.ManyToManyField('Condition')

    urgent = models.BooleanField(editable=False, default=False)

    pending = models.IntegerField(editable=False, default=0)

    last_msg = models.DateTimeField(blank=True, null=True, editable=False)

    sent_messages = models.ManyToManyField('AutomatedMessage')

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    def last_message(self):
        message = Message.objects.filter(client_id=self, sent_by='Client')
        if message.count() < 1:
            return "No messages yet"
        else:
            return message.reverse()[0]

    def update(self):
        messages = Message.objects.filter(client_id=self,
                                          sent_by='Client')
        self.last_msg = messages[0].date
        self.pending = len(messages.filter(read=False))
        self.urgent = (datetime.now() - self.last_msg) > URGENT
        self.save()
        


class Nurse(models.Model):

    id = models.IntegerField(primary_key=True)

    user = models.OneToOneField(User)

    location = models.ForeignKey(Location)
    
    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name

class Message(models.Model):

    class Meta:
        ordering = ['date']
        
    SENDER_CHOICES = (
        ('Client', 'Client'),
        ('Nurse', 'Nurse'),
        ('System', 'System'),
    )

    client_id = models.ForeignKey(Client)

    user_id = models.ForeignKey(Nurse)

    sent_by = models.CharField(max_length=6, choices=SENDER_CHOICES)

    content = models.CharField(max_length=500)

    date = models.DateTimeField(auto_now_add=True)

    read = models.BooleanField(default=False, editable=False)

    def __unicode__(self):
        return self.content


class SMSSyncOutgoing(models.Model):

    target = models.CharField(max_length=50)

    content = models.CharField(max_length=500)

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
