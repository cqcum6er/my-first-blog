from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):  #Create an admin class for customized admin interface.
	list_display = ('Day', 'Symbol', 'LastPrice')

admin.site.register(Post, PostAdmin)
