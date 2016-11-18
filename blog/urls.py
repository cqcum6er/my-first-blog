#blog.urls
from django.conf.urls import include, url
from . import views  #Import "views.py" in the current folder.
urlpatterns = [
    url(r'^$', views.home, name='home_link'),  #r'^$' indicates the start of the string and end of string regex symbols with nothing between them; 'http://127.0.0.1:8000/' is not a part of URL.
	url(r'^DJ_LastDay/', views.DJ_LastDay, name='DJ_link'),  #Include 'name' parameter for easy link reference in html file.
	url(r'^inProgress/', views.inProgrss, name ='inProgress_link'),  #For pages under construction.
]