from django import template

register = template.Library()

@register.filter
def mult(val, arg):  #, *args, **kwargs):
	if val:
		return float(val) * float(arg)
	else:
		return val

@register.filter
def sub(val, arg):
	if val:
		return float(val) - float(arg)
	else:
		return val

@register.filter
def div(val, arg):
	if val:
		return float(val) / float(arg)
	else:
		return val
