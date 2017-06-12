#blog.urls. Note that no html template name is used, only shortcut name in urls.py.
from django.conf.urls import include, url
from . import views  #Import "views.py" in the current folder to access view function.
urlpatterns = [
    url(r'^$', views.home, name='home_link'),  #r'^$' indicates the start of the string and end of string regex symbols with nothing inbetween; 'http://127.0.0.1:8000/' is not a part of URL.
	url(r'^DJ_LastDay/', views.DJ_LastDay, name='DJ_LastDay'),  #Include 'name' parameter for easy link reference in html file.
	url(r'^DJ_LastWeek/', views.DJ_LastWk, name='DJ_LastWk'),
	url(r'^DJ_LastMonth/', views.DJ_LastMnth, name='DJ_LastMnth'),
	url(r'^DJ_LastQuarter/', views.DJ_LastQtr, name='DJ_LastQtr'),
	url(r'^DJ_LastYear/', views.DJ_LastYr, name='DJ_LastYr'),
	#url(r'^NoData/', views.DJ_LastYr, name ='DJ_LastYr'),  #For pages under construction.
	url(r'^inProgress/', views.inProgrss, name ='inProgress_link'),  #For pages under construction.
	url(r'^feedback/', views.feedback_form, name='feedback'),
	url(r'^thanks/', views.thanks, name='thanks'),
	url(r'^EduCenter/', views.edu_center, name='EduCenter'),
	url(r'^results/', views.get_query, name='results'),
	#url(r'^results/(?P<Symbol>\d+)/', views.get_query, name='results'),  #(?P<name>pattern), where name is the name of the group and pattern is some pattern to match. The captured values are passed to view functions as keyword arguments rather than positional arguments. For example, the pk argument will be passed to views.get_query as a string object.
	url(r'^NoMatch/', views.get_query, name='NoMatch'),
]