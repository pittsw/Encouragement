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
				'source':{'safaricom':20687,'airtelkenya':6873}
				}
			}

	@classmethod
	def send(cls, client, content):
		"""Sends a message through the Shujaa protocol.
		"""
		#copy gateway values and add in phone number, message, and network
		cls.send_shujaa(client.phone_number,content,client.phone_network)
		
	@classmethod
	def send_shujaa(cls,destination,content,network):
		
		#get default values
		values = cls.gateway['values'].copy()
		
		values['destination'] = destination
		values['message'] = content
		values['network'] = network
		values['source'] = cls.gateway['values']['source'][network]
		
		#http request to getway to send sms
		data = urllib.urlencode(values)
		
		req = urllib2.Request(cls.gateway['url'], data)
		#print >>sys.stderr, "Shujaa Send: %s %s,%s"%(network,destination,content)
		
		#Send http request
		httpResponse = urllib2.urlopen(req)
		
		#do something with response 
		#response = httpResponse.read()
		#print >> sys.stderr, response
		
	@classmethod
	def send_batch(cls, lst):
		"""Sends all of the messages in lst.

		Arguments:
			lst - a list of (target, content) tuples like those that could be
				sent with send()

		"""
		for target, content in lst:
			cls.send(target, content)
		
		
        
