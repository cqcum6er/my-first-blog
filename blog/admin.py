#Customize display for each model under Django administration.
from django.contrib import admin
from .models import Post, NASDAQ_Post, SP500_Post, All_ks, Index_DJ, Index_SP500, UserComment
#from .forms import FeedbackForm  #Use if feedback form is linked to model instances.

class PostAdmin(admin.ModelAdmin):  #Create an admin class for customized admin interface.
	list_display = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'DivYild', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA']  #Choose attributes to display.
	list_display_links = ['Symbol']  #Specify linkable attribute under display.
	list_filter = ['Day', 'Symbol']  #Add filter function for admin page.
	search_fields = ['Day', 'Symbol', 'LastPrice']  #Implment search function for specific fields.
	list_per_page = 100
'''
	class Meta:  #Use if feedback form is linked to model instances.
		model = Post
'''
admin.site.register(Post, PostAdmin)  #Associate the admin object ('PostAdmin') with the model ('Post').

class SP500_Admin(admin.ModelAdmin):
	list_display = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'DivYild', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA']
	list_display_links = ['Symbol']
	list_filter = ['Day', 'Symbol']
	search_fields = ['Day', 'Symbol', 'LastPrice']
	list_per_page = 200

admin.site.register(SP500_Post, SP500_Admin)

class NASDAQ_Admin(admin.ModelAdmin):
	list_display = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'DivYild', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA']
	list_display_links = ['Symbol']
	list_filter = ['Day', 'Symbol']
	search_fields = ['Day', 'Symbol', 'LastPrice']
	list_per_page = 400

admin.site.register(NASDAQ_Post, NASDAQ_Admin)

class All_ks_Admin(admin.ModelAdmin):
	list_display = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'DivYild', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA']
	list_display_links = ['Symbol']
	list_filter = ['Day', 'Symbol']
	search_fields = ['Day', 'Symbol', 'LastPrice']
	list_per_page = 400

admin.site.register(All_ks, All_ks_Admin)

class Index_DJ_Admin(admin.ModelAdmin):
	list_display = ['Day', 'Symbol']
	list_display_links = ['Symbol']
	list_filter = ['Day', 'Symbol']
	search_fields = ['Day', 'Symbol']

admin.site.register(Index_DJ, Index_DJ_Admin)

class Index_SP500_Admin(admin.ModelAdmin):
	list_display = ['Day', 'Symbol']
	list_display_links = ['Symbol']
	list_filter = ['Day', 'Symbol']
	search_fields = ['Day', 'Symbol']
	list_per_page = 505

admin.site.register(Index_SP500, Index_SP500_Admin)

class CommentAdmin(admin.ModelAdmin):  #Create an admin class for customized admin interface.
	list_display = ('name', 'email')

admin.site.register(UserComment, CommentAdmin)