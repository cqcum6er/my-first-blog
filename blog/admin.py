from django.contrib import admin
from .models import Post
#from .forms import FeedbackForm  #Use if feedback form is linked to model instances.

class PostAdmin(admin.ModelAdmin):  #Create an admin class for customized admin interface.
	list_display = ('Day', 'Symbol', 'LastPrice')
'''
	class Meta:  #Use if feedback form is linked to model instances.
		model = Post
'''
admin.site.register(Post, PostAdmin)
#admin.site.register(FeedbackForm)  #Use if feedback form is linked to model instances.