#blog.urls
from django.conf.urls import include, url
from . import views  #Import "views.py" in the current folder to access view function.
urlpatterns = [
    url(r'^$', views.home, name='home_link'),  #r'^$' indicates the start of the string and end of string regex symbols with nothing between them; 'http://127.0.0.1:8000/' is not a part of URL.
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
	url(r'^results/(?P<pk>\d+)/$', views.query_search, name='results'),
]