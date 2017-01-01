from django.shortcuts import render
from django.utils import timezone
from .models import Post  #'Post' table object is retrieved from 'models.py' within the same folder.
from django.db.models import Max
import requests
import csv
import datetime
import aniso8601
'''
#Save scheduled csv record from Pythonanywhere, then run local server ONCE to populate local database before commenting out this block; comment out this block before saving views.py to Pythonanywhere to use scheduled csv instead...
#if not Post:  #Check to see if database is empty.  If it's not, do nothing, else empty existing entry to prepare for update. (Remove the 'if' statement if run as a scheduler command on Pythonanywhere.)
	#pass
#else:
Post.objects.all().delete()  #Clean the database before entry from csv file.
fields = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'FiftyTwoWkLo', 'FiftyTwoWkHi', 'DivYild', 'TrailPE', 'ForwardPE', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA', 'Name']  #Must match individual field (column) names in models.py.
with open('DJ_list.csv', 'rb') as file:  # Need to use absolute path when on Pythonanywhere server (i.e. use '/home/cqcum6er/my-first-blog/DJ_list.csv' as file path.)
	infile = csv.reader(file, delimiter=",", quotechar='"')  #Specify csv item boundary.
	for row in infile:
		Post.objects.create(**dict(zip(fields, row)))
#...end of block.
'''
def iso_to_gregorian(iso_year, iso_week, iso_day):  #Converts ISO week date format to Gregorian calendar date format.
    jan4 = datetime.date(iso_year, 1, 4)  #1st week ('Week 01') of new year always contains Jan 4th.
    start = jan4 - datetime.timedelta(days=jan4.isoweekday()-1)
    return start + datetime.timedelta(weeks=iso_week-1, days=iso_day-1)

def home(request):  #Home url
	return render(request, 'blog/home.html')

def inProgrss(request):  #In-Progress url
	return render(request, 'blog/InProgress.html')

def DJ_LastDay(request):  #"DJ_LastDay" must be requested from urls.py
	#posts = Post.objects.values()  #values() returns content of database as dictionary rather than model instances, making the database iterable.
	'''first_date = datetime.date(2016, 9, 16)
	last_date = datetime.date(2016, 9, 17)
	posts = Post.objects.filter(Day__range=(first_date, last_date))'''
	#posts = Post.objects.filter(Day__lte=timezone.now()).exclude(Day__lte=timezone.now() - datetime.timedelta(days=1))  #Retrieve all dates equal to or older than today but exclude those from yesterday or older; use timezone.now() instead of datetime.datetime.now() to avoid problems with timezones.
	#posts = Post.objects.values('Day').order_by('-Day').annotate(Max('Day'))
	p = Post.objects.latest('Day')  #Returns an object instance (not iterable); if latest() is empty, it works with attributes defined by 'class Meta' in models.py. Note latest () only retrieve ONE instance; .values() needs to be inserted in front of latest() to make it iterable as dictionary.
	posts = Post.objects.filter(Day=p.Day)  #Retrieve all instances with latest day ('p.Day') as QuerySet object.
	'''print type(p.Day)
	print p.Day
	print timezone.now()
	print iso_to_gregorian(timezone.now().isocalendar()[0], timezone.now().isocalendar()[1], 3)  #Convert Gregorian calendar date format to ISO week date format.
	testday = datetime.datetime.strptime('2017-01-01','%Y-%m-%d')  #Convert str to datetime object from datetime module.
	print testday
	print iso_to_gregorian(testday.isocalendar()[0], testday.isocalendar()[1]-1, 3)  #Show date from last week's Wednesday.'''
	return render(request, 'blog/DJ_LastDay.html', {'posts': posts})  #To serve as a template, 'blog/DJ.html' has to be put in blog\template\blog\
	#The last parameter, which looks like this: {} is a place to integrate objects in models.py (posts) with html ('posts') in template folder.

def DJ_LastWk(request):  #Display value from Wednesday of last week.
	p = Post.objects.latest('Day')  #Returns an object instance (not iterable); if latest() is empty, it works with attributes defined by 'class Meta' in models.py. Note latest () only retrieve ONE instance; .values() needs to be inserted in front of latest() to make it iterable as dictionary.
	LastDay = datetime.datetime.strptime(str(p.Day),'%Y-%m-%d')  #Convert str to datetime object from datetime module.
	'''print LastDay
	print iso_to_gregorian(LastDay.isocalendar()[0], LastDay.isocalendar()[1]-1, 3)  #Show date from last week's Wednesday.'''
	posts = Post.objects.filter(Day=iso_to_gregorian(LastDay.isocalendar()[0], LastDay.isocalendar()[1]-1, 3))  #Retrieve all instances from Wednesday of last week.
	return render(request, 'blog/DJ_LastWk.html', {'posts': posts})  #To serve as a template, 'blog/DJ.html' has to be put in blog\template\blog\
	#The last parameter, which looks like this: {} is a place to integrate objects in models.py (posts) with html ('posts') in template folder.
