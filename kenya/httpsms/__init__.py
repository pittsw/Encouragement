from transports import BaseTransport
from httpsms.models import HTTPSMSOutgoing
import urllib, urllib2

class Transport(BaseTransport):
	"""A transport that sends a message through an SMSSync API.

	"""

	gateway = {'url':'http://localhost:8888/shujaa/receive',
				'values':{
				'callbackType':'incomingSms',
				'destination':'6873',
				'account':'live',
				}
				}
				
	@classmethod
	def send(cls, client, content):
		"""Sends a message through the HTTPSMS protocol.
		"""
		HTTPSMSOutgoing(target=client.phone_number,network=client.phone_network, content=content).save()
		
