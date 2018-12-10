#mysite.urls
from django.conf.urls import include, url
from django.contrib import admin
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('blog.urls', namespace="blog")),  #Use 'include' to access all urls under 'blog' folder ('$' must not be present at the end of url string); use namespace for reference in template, i.e. <namespace>:<name>.
]

#urlpatterns += staticfiles_urlpatterns()