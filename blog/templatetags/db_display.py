from django import template

register = template.Library()
@register.inclusion_tag('results.html')
def show_results(Post):
	if arg == 'DJ_LastDay':
		p = Post.objects.latest('Day')
		posts = Post.objects.filter(Day=p.Day)
		return {'LastDay_posts': posts}
	elif arg == 'DJ_LastWk':
		p = Post.objects.latest('Day')
		LastDay = datetime.datetime.strptime(str(p.Day),'%Y-%m-%d')
		
	'''
	choices = Post.choice_set.all()
	return {'choices': choices}
	'''