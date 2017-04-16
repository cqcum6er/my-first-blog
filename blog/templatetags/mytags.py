from django import template

register = template.Library()

@register.simple_tag
def hour_range():
	"""
	Returns a list of hours in a day by 24 hour clock.
	"""
	return ["{0:0=2d}".format(x) for x in range(0,24)]