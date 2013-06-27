from transports import BaseTransport
import urllib, urllib2,sys

import shujaa.models as shujaa

class Transport(BaseTransport):
	"""A transport that sends a message through the Shujaa API.

	"""

	gateway = {'url':'http://sms2.shujaa.mobi/sendsms',
				'values':{
				'username':'bderenzi@cs.washington.edu',
				'password':'washington312',
				'account':'live',
				'source':{'safaricom':20687,'airtelkenya':6873}
				}
			}

	@classmethod
	def send(cls, client, content):
		"""Sends a message through the Shujaa protocol.
		"""
		
		cls.send_shujaa(client.phone_number,content,client.phone_network)
		
	@classmethod
	def send_shujaa(cls,destination,content,network):
		
		#copy gateway values and add in phone number, message, and network
		values = cls.gateway['values'].copy()
		
		values['destination'] = destination
		values['message'] = content
		values['network'] = network
		values['source'] = cls.gateway['values']['source'][network]
		
		message = shujaa.ShujaaMsg(client_number=destination,message=content,network=network)
		
		#http request to getway to send sms
		data = urllib.urlencode(values)
		
		req = urllib2.Request(cls.gateway['url'], data)
		#print >>sys.stderr, "Shujaa Send: %s %s,%s"%(network,destination,content)
		
		#Send http request
		#httpResponse = urllib2.urlopen(req)
		
		#do something with response 
		#smessage.response = httpResponse.read()
		#print >> sys.stderr, response
		
		message.save()
		
	@classmethod
	def send_batch(cls, lst):
		"""Sends all of the messages in lst.

		Arguments:
			lst - a list of (target, content) tuples like those that could be
				sent with send()

		"""
		for target, content in lst:
			cls.send(target, content)
		
		
        
