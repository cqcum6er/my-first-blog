#Customize display for each model under Django administration.
from django.contrib import admin
from .models import Post, UserComment
#from .forms import FeedbackForm  #Use if feedback form is linked to model instances.

class PostAdmin(admin.ModelAdmin):  #Create an admin class for customized admin interface.
	list_display = ['Day', 'Symbol', 'LastPrice']  #Choose attributes to display.
	list_display_links = ['Symbol']  #Specify linkable attribute under display.
	list_filter = ['Day', 'Symbol']  #Add filter function for admin page.
	search_fields = ['Day', 'Symbol', 'LastPrice']  #Implment search function.
'''
	class Meta:  #Use if feedback form is linked to model instances.
		model = Post
'''
admin.site.register(Post, PostAdmin)  #Associate the admin object ('PostAdmin') with the model ('Post').

class CommentAdmin(admin.ModelAdmin):  #Create an admin class for customized admin interface.
	list_display = ('name', 'email')

admin.site.register(UserComment, CommentAdmin)