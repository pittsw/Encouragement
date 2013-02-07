from transports import BaseTransport
import urllib, urllib2,sys

class Transport(BaseTransport):
	"""A transport that sends a message through the Shujaa API.

	"""

	gateway = {'url':'http://sms.shujaa.mobi/sendsms',
				'values':{
				'username':'bderenzi@cs.washington.edu',
				'password':'washington312',
				'account':'live',
				'source':'6873'}
				}

	@classmethod
	def send(cls, client, content):
		"""Sends a message through the Shujaa protocol.
		"""
		#copy gateway values and add in phone number, message, and network
		values = cls.gateway['values'].copy()
		values['destination'] = client.phone_number
		values['message'] = content
		values['network'] = client.phone_network
		
		#http request to getway to send sms
		data = urllib.urlencode(values)
		req = urllib2.Request(cls.gateway['url'], data)
		#print >>sys.stderr, "Shujaa Send: %s %s,%s"%(client.phone_network,client.phone_number,content)
		''' Don't Send Now '''
		httpResponse = urllib2.urlopen(req)
		
		#do something with response 
		response = httpResponse.read()
		print >> sys.stderr, response
		
	@classmethod
	def send_batch(cls, lst):
		"""Sends all of the messages in lst.

		Arguments:
			lst - a list of (target, content) tuples like those that could be
				sent with send()

		"""
		for target, content in lst:
			cls.send(target, content)
		
		
        
