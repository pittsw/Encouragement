from django import template
import json

register = template.Library()

@register.filter
def klass(obj):
    return obj.__class__.__name__
    
@register.filter
def dictlookup(value,arg):
	try:
		return json.loads(arg)[str(value)]
	except Exception as e:
		return value
