#Customize display for each model under Django administration.
from django.contrib import admin
from django.forms import Textarea  #To implement widget modification of message area.
from django.db import models  #To implement widget modification of message area.
from .models import Post, NASDAQ_Post, SP500_Post, Index_DJ, Index_SP500, UserComment, sp500_post_sorted, all_ks_join, all_ks_join_unique, all_ks, all_ks_DatePriceDiff
#from .forms import FeedbackForm  #Use if feedback form is linked to model instances.

class PostAdmin(admin.ModelAdmin):  #Create an admin class for customized admin interface.
	list_display = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'DivYild', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA']  #Choose attributes to display.
	list_display_links = ['Symbol']  #Specify linkable attribute under display.
	list_filter = ['Day', 'Symbol']  #Add filter function for admin page.
	search_fields = ['Symbol', 'Name']  #Implment search function for specific fields.
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
	search_fields = ['Symbol', 'Name']
	list_per_page = 200

admin.site.register(SP500_Post, SP500_Admin)

class NASDAQ_Admin(admin.ModelAdmin):
	list_display = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'DivYild', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA']
	list_display_links = ['Symbol']
	list_filter = ['Day', 'Symbol']
	search_fields = ['Symbol', 'Name']
	list_per_page = 400

admin.site.register(NASDAQ_Post, NASDAQ_Admin)

class sp500_post_sorted_Admin(admin.ModelAdmin):
	list_display = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'DivYild', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA']
	list_display_links = ['Symbol']
	list_filter = ['Day', 'Symbol']
	search_fields = ['Symbol', 'Name']
	list_per_page = 400

admin.site.register(sp500_post_sorted, sp500_post_sorted_Admin)

class all_ks_Admin(admin.ModelAdmin):
	list_display = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'DivYild', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA', 'Sector']
	list_display_links = ['Symbol']
	list_filter = ['Day', 'Symbol']
	search_fields = ['Symbol', 'Name']
	date_hierarchy = 'Day'  #Filter data by years and months (see https://medium.com/@hakibenita/scaling-django-admin-date-hierarchy-85c8e441dd4c)
	list_per_page = 400

admin.site.register(all_ks, all_ks_Admin)

class all_ks_DatePriceDiff_Admin(admin.ModelAdmin):
	list_display = ['Day', 'Name', 'Symbol', 'Price_1', 'Price_7', 'Price_30']
	list_display_links = ['Symbol']
	list_filter = ['Day', 'Symbol']
	search_fields = ['Symbol', 'Name']
	list_per_page = 400

admin.site.register(all_ks_DatePriceDiff, all_ks_DatePriceDiff_Admin)

class all_ks_join_Admin(admin.ModelAdmin):
	list_display = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'DivYild', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA']
	list_display_links = ['Symbol']
	list_filter = ['Day', 'Symbol']
	search_fields = ['Symbol', 'Name']
	list_per_page = 400

admin.site.register(all_ks_join, all_ks_join_Admin)

class all_ks_join_unique_Admin(admin.ModelAdmin):
	list_display = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'DivYild', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA']
	list_display_links = ['Symbol']
	list_filter = ['Day', 'Symbol']
	search_fields = ['Symbol', 'Name']
	list_per_page = 400

admin.site.register(all_ks_join_unique, all_ks_join_unique_Admin)

class Index_DJ_Admin(admin.ModelAdmin):
	list_display = ['Day', 'Symbol']
	list_display_links = ['Symbol']
	list_filter = ['Day', 'Symbol']
	search_fields = ['Symbol']

admin.site.register(Index_DJ, Index_DJ_Admin)

class Index_SP500_Admin(admin.ModelAdmin):
	list_display = ['Day', 'Symbol']
	list_display_links = ['Symbol']
	list_filter = ['Day', 'Symbol']
	search_fields = ['Symbol']
	list_per_page = 505

admin.site.register(Index_SP500, Index_SP500_Admin)

class CommentAdmin(admin.ModelAdmin):  #Create an admin class for customized admin interface.
	list_display = ['created_at', 'name', 'email']
	readonly_fields = ['created_at']  #For use with models.DateTimeField(auto_now_add=True) to display the hidden field.
	list_display_links = ['name']
	list_filter = ['created_at', 'name', 'email']
	search_fields = ['name', 'email', 'message']
	formfield_overrides = {
		models.TextField: {'widget': Textarea(attrs={'rows':16, 'cols':80})},
	}  #Increase viewable area with widget.

admin.site.register(UserComment, CommentAdmin)