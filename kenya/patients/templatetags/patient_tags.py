from django import template

register = template.Library()

@register.filter
def klass(obj):
    return obj.__class__.__name__
