from django.contrib import admin
from .models import Post

#class PostAdmin(admin.ModelAdmin):  #Allow organization of individual 'Post' table entry.
	#date_hierarchy = 'created_date'
	#list_display = ('title', 'author', 'created_date')
	
#admin.site.register(Post, PostAdmin)
admin.site.register(Post)