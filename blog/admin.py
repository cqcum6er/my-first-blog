#Customize display for each model under Django administration.
from django.contrib import admin
from .models import Post, UserComment, NASDAQ_Post
#from .forms import FeedbackForm  #Use if feedback form is linked to model instances.

class PostAdmin(admin.ModelAdmin):  #Create an admin class for customized admin interface.
	list_display = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'DivYild', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA']  #Choose attributes to display.
	list_display_links = ['Symbol']  #Specify linkable attribute under display.
	list_filter = ['Day', 'Symbol']  #Add filter function for admin page.
	search_fields = ['Day', 'Symbol', 'LastPrice']  #Implment search function for specific fields.
'''
	class Meta:  #Use if feedback form is linked to model instances.
		model = Post
'''
admin.site.register(Post, PostAdmin)  #Associate the admin object ('PostAdmin') with the model ('Post').

class NASDAQ_Admin(admin.ModelAdmin):
	list_display = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'DivYild', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA']
	list_display_links = ['Symbol']
	list_filter = ['Day', 'Symbol']
	search_fields = ['Day', 'Symbol', 'LastPrice']
	
admin.site.register(NASDAQ_Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):  #Create an admin class for customized admin interface.
	list_display = ('name', 'email')

admin.site.register(UserComment, CommentAdmin)