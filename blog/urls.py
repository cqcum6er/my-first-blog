#blog.urls. Note that no html template name is used, only shortcut name in urls.py. Each distinct page has its own url path, even if most other elements within the page remain the same.
from django.conf.urls import include, url
from . import views  #Import "views.py" in the current folder to access view function.
urlpatterns = [
    url(r'^$', views.home, name='home_link'),  #r'^$' indicates the start of the string and end of string regex symbols with nothing inbetween; 'http://127.0.0.1:8000/' (or IP address of local server) is not a part of URL; URL string can be arbitray and different from html template name.
	url(r'^DJ_LastDay/', views.DJ_LastDay, name='DJ_LastDay'),  #Include 'name' parameter for easy link reference in html file.
	url(r'^DJ_LastWeek/', views.DJ_LastWk, name='DJ_LastWk'),
	url(r'^DJ_LastMonth/', views.DJ_LastMnth, name='DJ_LastMnth'),
	url(r'^DJ_LastQuarter/', views.DJ_LastQtr, name='DJ_LastQtr'),
	url(r'^DJ_Last6Month/', views.DJ_Last6Mnth, name='DJ_Last6Mnth'),
	url(r'^DJ_LastYear/', views.DJ_LastYr, name='DJ_LastYr'),
	url(r'^SP_LastDay/', views.SP_LastDay, name='SP_LastDay'),
	url(r'^SP_LastWeek/', views.SP_LastWk, name='SP_LastWk'),
	url(r'^SP_LastMonth/', views.SP_LastMnth, name='SP_LastMnth'),
	url(r'^SP_LastQuarter/', views.SP_LastQtr, name='SP_LastQtr'),
	url(r'^SP_Last6Month/', views.SP_Last6Mnth, name='SP_Last6Mnth'),
	url(r'^SP_LastYear/', views.SP_LastYr, name='SP_LastYr'),
	url(r'^About/', views.AboutMe, name ='AboutMe_link'),  #For pages under construction.
	url(r'^Contact/', views.contact_form, name='contact_link'),
	url(r'^Thanks/', views.thanks, name='thanks'),
	url(r'^Resources_Definitions/', views.ResCenter_Def, name='ResCenter_link'),
	url(r'^Resources_Links/', views.ResCenter_Links, name='ResCenter_Links_link'),
	url(r'^Resources_Plugs/', views.ResCenter_Plugs, name='ResCenter_Plugs_link'),
	#url(r'^movers/', views.get_query, name='movers'),
	url(r'^results/', views.get_query, name='results'),
	#url(r'^results/(?P<Symbol>\d+)/', views.get_query, name='results'),  #(?P<name>pattern), where name is the name of the group and pattern is some pattern to match. The captured values are passed to view functions as keyword arguments rather than positional arguments. For example, the pk argument will be passed to views.get_query as a string object.
	#url(r'^NoMatch/', views.get_query, name='NoMatch'),
	url(r'^Indices_LastWeek/', views.Ind_LastWk, name='Ind_LastWk'),
	url(r'^Indices_LastQuarter/', views.Ind_LastQtr, name='Ind_LastQtr'),
	url(r'^Indices_Last6Months/', views.Ind_Last6Mnth, name='Ind_Last6Mnth'),
	url(r'^Indices_LastYear/', views.Ind_LastYr, name='Ind_LastYr'),
	url(r'^Indices_Last5Year/', views.Ind_Last5Yr, name='Ind_Last5Yr'),
]