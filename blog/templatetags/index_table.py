'''
index_table.py allows multiple base templates to share a child template, with context altered for each child. Usage:
{% block content %}
	...
	{% load index_table %}
	{% DJ_LastDay %}
	...
{% endblock %}
'''
from django import template

register = template.Library()

@register.inclusion_tag('blog/index_table.html', takes_context=True)
def DJ_LastDay(context):
	return {'posts':context['DJ_LastDay_posts'], 'request':context['request']}

@register.inclusion_tag('blog/index_table.html', takes_context=True)
def DJ_LastWk(context):
	return {'posts': context['DJ_LastWk_posts'], 'request':context['request']}

@register.inclusion_tag('blog/index_table.html', takes_context=True)
def DJ_LastMnth(context):
	return {'posts': context['DJ_LastMnth_posts'], 'request':context['request']}

@register.inclusion_tag('blog/index_table.html', takes_context=True)
def DJ_LastQtr(context):
	return {'posts': context['DJ_LastQtr_posts'], 'request':context['request']}

@register.inclusion_tag('blog/index_table.html', takes_context=True)
def DJ_Last6Mnth(context):
	return {'posts': context['DJ_Last6Mnth_posts'], 'request':context['request']}

@register.inclusion_tag('blog/index_table.html', takes_context=True)
def DJ_LastYr(context):
	return {'posts': context['DJ_LastYr_posts'], 'request':context['request']}