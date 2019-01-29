'''
table_index.py allows multiple base templates to share a child template, with context altered for each child. Usage:
{% block content %}
	...
	{% load table_index %}
	{% DJ_LastDay %}
	...
{% endblock %}
'''
from django import template

register = template.Library()

@register.inclusion_tag('blog/table_index.html', takes_context=True)
def DJ_LastDay(context):  #DJ_LastDay defined by a function in views.py.
	return {'posts':context['DJ_LastDay_posts'], 'request':context['request']}  #Arg inside context[] are taken from views.py; arg in front of context[] are found in HTML.

@register.inclusion_tag('blog/table_index.html', takes_context=True)
def SP_LastDay(context):
	return {'posts':context['SP_LastDay_posts'], 'request':context['request']}

@register.inclusion_tag('blog/table_index.html', takes_context=True)
def DJ_LastWk(context):
	return {'posts': context['DJ_LastWk_posts'], 'request':context['request']}

@register.inclusion_tag('blog/table_index.html', takes_context=True)
def SP_LastWk(context):
	return {'posts': context['SP_LastWk_posts'], 'request':context['request']}

@register.inclusion_tag('blog/table_index.html', takes_context=True)
def DJ_LastMnth(context):
	return {'posts': context['DJ_LastMnth_posts'], 'request':context['request']}

@register.inclusion_tag('blog/table_index.html', takes_context=True)
def SP_LastMnth(context):
	return {'posts': context['SP_LastMnth_posts'], 'request':context['request']}

@register.inclusion_tag('blog/table_index.html', takes_context=True)
def DJ_LastQtr(context):
	return {'posts': context['DJ_LastQtr_posts'], 'request':context['request']}

@register.inclusion_tag('blog/table_index.html', takes_context=True)
def SP_LastQtr(context):
	return {'posts': context['SP_LastQtr_posts'], 'request':context['request']}

@register.inclusion_tag('blog/table_index.html', takes_context=True)
def DJ_Last6Mnth(context):
	return {'posts': context['DJ_Last6Mnth_posts'], 'request':context['request']}

@register.inclusion_tag('blog/table_index.html', takes_context=True)
def SP_Last6Mnth(context):
	return {'posts': context['SP_Last6Mnth_posts'], 'request':context['request']}

@register.inclusion_tag('blog/table_index.html', takes_context=True)
def DJ_LastYr(context):
	return {'posts': context['DJ_LastYr_posts'], 'request':context['request']}

@register.inclusion_tag('blog/table_index.html', takes_context=True)
def SP_LastYr(context):
	return {'posts': context['SP_LastYr_posts'], 'request':context['request']}