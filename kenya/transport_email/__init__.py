from django.conf import settings
from transports import BaseTransport

#Email Imports
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


class Transport(BaseTransport):
	
	templates = {
		'number_change':'%s %s (%s) sent vaid key on %s old number %s\nNetwork:%s -> %s',
		'no_number':'%s not in database\n\nMessage\n\n%s',
	}

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
	def email(cls,subject,content):
		msg = MIMEMultipart()
		msg['From'] = settings.EMAIL['From']
		msg['To'] = settings.EMAIL['To']
		msg['Subject'] = "Mobile WaCH: %s"%(subject)
		msg.attach(MIMEText(content))
		
		mailServer = smtplib.SMTP("smtp.gmail.com",587)
		mailServer.ehlo();mailServer.starttls();mailServer.ehlo()
		
		mailServer.login(settings.EMAIL['From'],settings.EMAIL['Password'])
		mailServer.sendmail(settings.EMAIL['From'],settings.EMAIL['To'],msg.as_string())
		
		mailServer.close()
