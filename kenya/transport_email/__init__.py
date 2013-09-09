from django.conf import settings
from transports import BaseTransport

#Email Imports
import smtplib,sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from backend.models import Email as EmailTemplates


class Transport(BaseTransport):
	
	@classmethod
	def send(cls, client, content):
		#print "Sending SMS As Email"
		cls.email("SMS as Email to %s(%s) on %s"%(client.nickname,client.phone_number,client.phone_network),content)

	@classmethod
	def send_batch(cls, lst):
		"""Sends all of the messages in lst.

		Arguments:
			lst - a list of (target, content) tuples like those that could be
				sent with send()

		"""
		for target, content in lst:
			cls.send(target, content)
			
	@classmethod
	def template_email(cls,template,**keys):
		try:
			template = EmailTemplates.objects.get(key=template)
			cls.email(template.subject.format(**keys),template.content.format(**keys))
		except Exception as e:
			print >> sys.stderr, "Email Template Not Found"
	
	@classmethod
	def email(cls,subject,content,group='debug'):
		msg = MIMEMultipart()
		msg['From'] = settings.EMAIL['From']
		msg['To'] = settings.EMAIL['To'][group]
		msg['Subject'] = "Mobile WaCH: %s"%(subject)
		msg.attach(MIMEText(content))
		
		mailServer = smtplib.SMTP("smtp.gmail.com",587)
		mailServer.ehlo();mailServer.starttls();mailServer.ehlo()
		
		mailServer.login(settings.EMAIL['From'],settings.EMAIL['Password'])
		mailServer.sendmail(msg['From'],msg['To'].split(','),msg.as_string())
		
		mailServer.close()
