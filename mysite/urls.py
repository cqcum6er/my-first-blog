#mysite.urls
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('blog.urls', namespace="blog")),  #Use 'include' to access all blog-related url; use namespace for reference in template, i.e. <namespace>:<name>.
]
