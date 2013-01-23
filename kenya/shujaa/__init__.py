from transports import BaseTransport
import urllib, urllib2

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
	def send(cls, target, content):
		"""Sends a message through the Shujaa protocol.
		"""
		#copy gateway values and add in phone number, message, and network
		values = cls.gateway['values'].copy()
		values['destination'] = target
		values['message'] = content
		values['network'] = 'safaricom' #change this to get netowrk from target
		
		#http request to getway to send sms
		data = urllib.urlencode(values)
		req = urllib2.Request(cls.gateway['url'], data)
		#print "Shujaa Send: %s,%s"%(target,content)
		
		''' Don't Send Now '''
		httpResponse = urllib2.urlopen(req)
		
		#do something with response 
		response = httpResponse.read()
		#print response
		
		
		
		
        
