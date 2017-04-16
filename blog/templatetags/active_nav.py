from django import template
import re
#from django.core.urlresolvers import reverse, NoReverseMatch

register = template.Library()

#@register.simple_tag(takes_context=True) 
'''
def active(request, url):
	url_name = resolve(request.path).url_name
	if url_name == url:
		return "active"
	return ""
'''
'''
def active(context, urlnames):
    if context['request'].resolver_match.url_name in urlnames.split():
        return 'active'
    else:
        return ''
'''	
@register.simple_tag
def active(request, pattern):
	if re.search(pattern, request.path):
		return 'active'
	return ''

