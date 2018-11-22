#Enable dictionary variable key lookup with filter.
from django import template

register = template.Library()

@register.filter
def keyval(dict, key):
	return dict.get(key, '')
'''
def lookup(val, key):
	return val.get(key, '') #[])
'''

