from django.conf.urls import include, url
from . import views  #Import "views.py" in the current folder.
urlpatterns = [
    url(r'^$', views.post_list),  #r'^$' indicates the start of the string and end of string regex symbols with nothing between them; 'http://127.0.0.1:8000/' is not a part of URL
]