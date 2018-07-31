#views.py retrieves model instances from the database or instantiate a form (see feedback_form).
from django.shortcuts import render  #, render_to_response, redirect #get_object_or_404
#from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist  #Display in-app message when an instance isn't found.
#from django.http import HttpResponse
#from django.template import RequestContext
from difflib import get_close_matches  #Allow 'approximate' search.
'''
from django.db.models import Q  #Allow simultaneous search in different fields.
#For email.
from django.core.mail import EmailMessage, send_mail
from django.template import Context
from django.template.loader import get_template
'''
from .models import Post, SP500_Post, UserComment, Index_DJ, Index_SP500, all_ks  #Retrieve model objects from 'models.py' within the same folder.
from .forms import ContactForm
#from .templatetags import index_table
import datetime

'''
#To update database with the current date, save scheduled csv record from Pythonanywhere, then run local server ONCE to populate local database before commenting out this block; will need to remove duplicate rows with sqlite command afterward; comment out this block before uploading views.py to Pythonanywhere to use scheduled csv instead...
import csv
#if not Post:  #Check to see if database is empty.  If it's not, do nothing, else empty existing entry to prepare for update. (Remove the 'if' statement if run as a scheduler command on Pythonanywhere.)
	#pass
#else:
	#all_ks.objects.all().delete()
#all_ks.objects.all().delete()  #Clean the database before entry from csv file (If tables was dropped by SQL command, the table structure must be created 1st).
p = all_ks.objects.latest('Day')  #p = Post.objects.latest('Day')  #Check what's the lastest day then append to db from then on.
fields = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'FiftyTwoWkLo', 'FiftyTwoWkHi', 'DivYild', 'TrailPE', 'ForwardPE', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA', 'Name']  #Must match individual field (column) names in models.py.
with open('DJ_list.csv', 'rb') as file:  # Need to use absolute path when on Pythonanywhere server (i.e. use '/home/cqcum6er/my-first-blog/DJ_list.csv' as file path.)
	infile = csv.reader(file, delimiter=",", quotechar='"')  #Specify csv item boundary.
	for row in infile:
		row_datetime = datetime.datetime.strptime(row[0],'%Y-%m-%d')  #row[0] is converted from str to datetime format (i.e. '2017-08-27').
		#print row_datetime.date()
		row_date = row_datetime.date()  #Converting from datetime to date.
		if row_date > p.Day:  #Only append entry if the date of the entry is later than the most recent in db.
			#print row_date
			all_ks.objects.create(**dict(zip(fields, row)))
with open('SP500_list.csv', 'rb') as file:
	infile = csv.reader(file, delimiter=",", quotechar='"')
	for row in infile:
		row_datetime = datetime.datetime.strptime(row[0],'%Y-%m-%d')
		row_date = row_datetime.date()
		if row_date > p.Day:
			all_ks.objects.create(**dict(zip(fields, row)))
#...end of block.
'''

def DailyMovers():
	p = Post.objects.latest('Day')  #Returns an object instance (not iterable); if latest() is empty, it works with attributes defined by 'class Meta' in models.py. Note latest () only retrieve ONE instance; .values() needs to be inserted in front of latest() to make it iterable as dictionary; cache queryset object for quick retrieval in html request.
	#print p.LastPrice, type(p.LastPrice)
	posts = Post.objects.filter(Day=p.Day)
	Yesterday = p.Day - datetime.timedelta(days=1)  #Get datetime for yesterday.
	Movers = []
	for post in posts:
		ypost = Post.objects.filter(Day=Yesterday).filter(Symbol=post.Symbol).first()  #Use .first() or '[0]' with filter to get the first entry in queryset.
		#print post.Symbol, post.LastPrice, type(post.LastPrice), ypost.LastPrice, type(ypost.LastPrice),
		if post.LastPrice == "N/A" or ypost.LastPrice == "N/A":
			PercDayMov = 0.0
		else:
			PercDayMov = ((float(post.LastPrice) - float(ypost.LastPrice))/float(ypost.LastPrice))*100
		#print PercDayMov
		Movers.append(tuple((post.Symbol, post.Name, PercDayMov)))  #Add each symbol and it daily % movement as a tuple to a list ('Movers').
	Movers.sort(key=lambda tup: tup[2])  #Sort based on daily % movement (or 3rd element of each tuple).
	#print Movers, type(Movers)
	return Movers

def home(request):
	return render(request, 'blog/home.html', {'DailyMovers': DailyMovers()})

def Ind_LastWk(request):
	return render(request, 'blog/Indices_LastWeek.html', {'DailyMovers': DailyMovers()})

def Ind_LastQtr(request):
	return render(request, 'blog/Indices_LastQuarter.html', {'DailyMovers': DailyMovers()})

def Ind_Last6Mnth(request):
	return render(request, 'blog/Indices_Last6Months.html', {'DailyMovers': DailyMovers()})

def Ind_LastYr(request):
	return render(request, 'blog/Indices_LastYear.html', {'DailyMovers': DailyMovers()})

def Ind_Last5Yr(request):
	return render(request, 'blog/Indices_Last5Years.html', {'DailyMovers': DailyMovers()})

def ResCenter_Def(request):
	return render(request, 'blog/ResCenter_Def.html')

def	ResCenter_Links(request):
	return render(request, 'blog/ResCenter_Links.html')

def iso_to_gregorian(iso_year, iso_week, iso_day):  #Converts ISO week date format to Gregorian calendar date format.
	jan4 = datetime.date(iso_year, 1, 4)  #1st week ('Week 01') of new year always contains Jan 4th.
	start = jan4 - datetime.timedelta(days=jan4.isoweekday()-1)  #Get the year for ISO week date.
	return start + datetime.timedelta(weeks=iso_week-1, days=iso_day-1)
	
def DJ_LastDay(request):  #"DJ_LastDay" must be requested from urls.py
	try:
		#posts = Post.objects.values()  #values() returns content of database as dictionary rather than model instances, making the database iterable.
		#posts = Post.objects.filter(Day__lte=timezone.now()).exclude(Day__lte=timezone.now() - datetime.timedelta(days=1))  #Retrieve all dates equal to or older than today but exclude those from yesterday or older; use timezone.now() instead of datetime.datetime.now() to avoid problems with timezones.
		p = Index_DJ.objects.latest('Day') #p = Post.objects.latest('Day') #  #Returns an object instance (not iterable); if latest() is empty, it works with attributes defined by 'class Meta' in models.py. Note latest () only retrieve ONE instance; .values() needs to be inserted in front of latest() to make it iterable as dictionary; cache queryset object for quick retrieval in html request.
		#print p.Day
		Latest_DJ_Ind = Index_DJ.objects.filter(Day=p.Day)  #All symbols from the latest days of DJ index.
		#print Latest_DJ_Ind.count(), type(tuple(Latest_DJ_Ind)), tuple(Latest_DJ_Ind)
		posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(Latest_DJ_Ind))  #Retrieve all instances from latest day ('p.Day') that have all DJ index symbols.
		#print posts.count()
		if posts:  #Check for empty set.
			return render(request, 'blog/DJ_LastDay.html', {'DJ_LastDay_posts': posts})  #To serve as a template, 'blog/DJ.html' has to be put in blog\template\blog\
			#The last parameter, which looks like this: {} is a place to integrate objects in models.py (posts) with html ('posts') in template folder.
			#return HttpResponse(index_table.DJ_LastDay(context))
			#return render_to_response('blog/DJ_LastDay.html', {}, context_instance=RequestContext(request))
		else:
			return render(request, 'blog/NoPeriod.html')
	except ObjectDoesNotExist:  #Check for nonexistent set.
			return render(request, 'blog/NoPeriod.html')

def SP_LastDay(request):
	try:
		p = Index_SP500.objects.latest('Day')
		Latest_SP500_Ind = Index_SP500.objects.filter(Day=p.Day)
		posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(Latest_SP500_Ind))
		if posts:  #Check for empty set.
			return render(request, 'blog/SP_LastDay.html', {'SP_LastDay_posts': posts})
		else:
			return render(request, 'blog/NoPeriod_SP.html')
	except ObjectDoesNotExist:  #Check for nonexistent set.
			return render(request, 'blog/NoPeriod.html')

def DJ_LastWk(request):  #Display value from Wednesday of last week.
	try:
		p = Index_DJ.objects.latest('Day')
		#LastDay = datetime.datetime.strptime(str(p.Day),'%Y-%m-%d')  #Convert str to datetime object from datetime module (for use with isocalendar()).
		#print type(p.Day), type(LastDay)
		#print iso_to_gregorian(LastDay.isocalendar()[0], LastDay.isocalendar()[1]-1, 3)  #Show date from last Wednesday.
		LastWk_DJ_Ind = Index_DJ.objects.filter(Day=iso_to_gregorian(p.Day.isocalendar()[0], p.Day.isocalendar()[1]-1, 3))  #All symbols from the last Wednesday of DJ index.
		#print type(list(LastWk_DJ_Ind)), list(LastWk_DJ_Ind)
		d = iso_to_gregorian(p.Day.isocalendar()[0], p.Day.isocalendar()[1]-1, 3)
		#print type(d), d
		posts = all_ks.objects.filter(Day=d, Symbol__in=list(LastWk_DJ_Ind))  #Retrieve all key stats from last Wednesday that are present in DJ index; p.Day.isocalendar()[0] retrieves current year, & p.Day.isocalendar()[1] retrieves the current ISO week, and the last arg "3" retrieves Wed of that week.
		#print posts
		if posts:
			return render(request, 'blog/DJ_LastWk.html', {'DJ_LastWk_posts': posts})
		else:
			return render(request, 'blog/NoPeriod.html')
	except ObjectDoesNotExist:
			return render(request, 'blog/NoPeriod.html')

def SP_LastWk(request):
	try:
		p = Index_SP500.objects.latest('Day')
		#LastDay = datetime.datetime.strptime(str(p.Day),'%Y-%m-%d')
		LastWk_SP_Ind = Index_SP500.objects.filter(Day=iso_to_gregorian(p.Day.isocalendar()[0], p.Day.isocalendar()[1]-1, 3))
		d = iso_to_gregorian(p.Day.isocalendar()[0], p.Day.isocalendar()[1]-1, 3)
		posts = all_ks.objects.filter(Day=d, Symbol__in=list(LastWk_SP_Ind))
		if posts:
			return render(request, 'blog/SP_LastWk.html', {'SP_LastWk_posts': posts})
		else:
			return render(request, 'blog/NoPeriod_SP.html')
	except ObjectDoesNotExist:
			return render(request, 'blog/NoPeriod.html')

def DJ_LastMnth(request):  #Display value from the 1st (trading) day of last month.
	p = Index_DJ.objects.latest('Day')
	LastDay = datetime.datetime.strptime(str(p.Day),'%Y-%m-%d')
	CurrYr = LastDay.strftime('%Y')  #Retrieve current year as string from datetime object, LastDay.
	CurrMnth = LastDay.strftime('%m')  #Retrieve current month as string from datetime object, LastDay.
	if int(CurrMnth) >= 2:  #Check whether last month is still within the same year.
		try:
			p = Index_DJ.objects.filter(Day__year=CurrYr, Day__month=str(int(CurrMnth)-1)).earliest('Day')  #Retrieve earliest date available from last month.
			#print p.Day
			LastMnth_DJ_Ind = Index_DJ.objects.filter(Day=p.Day)
			#print type(LastMnth_DJ_Ind), LastMnth_DJ_Ind
			posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(LastMnth_DJ_Ind))
			if posts:
				return render(request, 'blog/DJ_LastMnth.html', {'DJ_LastMnth_posts': posts})
			else:
				return render(request, 'blog/NoPeriod.html')
		except ObjectDoesNotExist:
			return render(request, 'blog/NoPeriod.html')
	else:
		try:
			p = Index_DJ.objects.filter(Day__year=str(int(CurrYr)-1), Day__month=str(int(CurrMnth)+11)).earliest('Day')
			#print p.Day
			LastMnth_DJ_Ind = Index_DJ.objects.filter(Day=p.Day)
			posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(LastMnth_DJ_Ind))
			if posts:
				return render(request, 'blog/DJ_LastMnth.html', {'DJ_LastMnth_posts': posts})
			else:
				return render(request, 'blog/NoPeriod.html')
		except ObjectDoesNotExist:
			return render(request, 'blog/NoPeriod.html')

def SP_LastMnth(request):
	p = Index_SP500.objects.latest('Day')
	LastDay = datetime.datetime.strptime(str(p.Day),'%Y-%m-%d')
	CurrYr = LastDay.strftime('%Y')
	CurrMnth = LastDay.strftime('%m')
	if int(CurrMnth) >= 2:
		try:
			p = Index_SP500.objects.filter(Day__year=CurrYr, Day__month=str(int(CurrMnth)-1)).earliest('Day')
			LastMnth_SP_Ind = Index_SP500.objects.filter(Day=p.Day)
			posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(LastMnth_SP_Ind))
			if posts:
				return render(request, 'blog/SP_LastMnth.html', {'SP_LastMnth_posts': posts})
			else:
				return render(request, 'blog/NoPeriod_SP.html')
		except ObjectDoesNotExist:
			return render(request, 'blog/NoPeriod.html')
	else:
		try:
			p = Index_SP500.objects.filter(Day__year=str(int(CurrYr)-1), Day__month=str(int(CurrMnth)+11)).earliest('Day')
			LastMnth_SP_Ind = Index_SP500.objects.filter(Day=p.Day)
			posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(LastMnth_SP_Ind))
			if posts:
				return render(request, 'blog/SP_LastMnth.html', {'SP_LastMnth_posts': posts})
			else:
				return render(request, 'blog/NoPeriod_SP.html')
		except ObjectDoesNotExist:
			return render(request, 'blog/NoPeriod.html')

def DJ_LastQtr(request):  #Display value from the 1st (trading) day of last quarter.
	p = Index_DJ.objects.latest('Day')
	LastDay = datetime.datetime.strptime(str(p.Day),'%Y-%m-%d')
	CurrYr = LastDay.strftime('%Y')
	CurrMnth = LastDay.strftime('%m')
	if int(CurrMnth) >= 4:  #Check whether last quarter is still within the same year.
		try:
			p = Index_DJ.objects.filter(Day__year=CurrYr, Day__month=str(int(CurrMnth)-3)).earliest('Day')
			LastQtr_DJ_Ind = Index_DJ.objects.filter(Day=p.Day)
			posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(LastQtr_DJ_Ind))
			#print posts, posts.count()
			return render(request, 'blog/DJ_LastQtr.html', {'DJ_LastQtr_posts': posts})
		except ObjectDoesNotExist:
			return render(request, 'blog/NoPeriod.html')
	else:
		try:
			p = Index_DJ.objects.filter(Day__year=str(int(CurrYr)-1), Day__month=str(int(CurrMnth)+9)).earliest('Day')
			LastQtr_DJ_Ind = Index_DJ.objects.filter(Day=p.Day)
			posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(LastQtr_DJ_Ind))
			#print posts.count()
			return render(request, 'blog/DJ_LastQtr.html', {'DJ_LastQtr_posts': posts})
		except ObjectDoesNotExist:
			return render(request, 'blog/NoPeriod.html')

def SP_LastQtr(request):
	p = Index_SP500.objects.latest('Day')
	LastDay = datetime.datetime.strptime(str(p.Day),'%Y-%m-%d')
	CurrYr = LastDay.strftime('%Y')
	CurrMnth = LastDay.strftime('%m')
	if int(CurrMnth) >= 4:
		try:
			p = Index_SP500.objects.filter(Day__year=CurrYr, Day__month=str(int(CurrMnth)-3)).earliest('Day')
			LastQtr_SP_Ind = Index_SP500.objects.filter(Day=p.Day)
			posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(LastQtr_SP_Ind))
			return render(request, 'blog/SP_LastQtr.html', {'SP_LastQtr_posts': posts})
		except ObjectDoesNotExist:
			return render(request, 'blog/NoPeriod_SP.html')
	else:
		try:
			p = Index_SP500.objects.filter(Day__year=str(int(CurrYr)-1), Day__month=str(int(CurrMnth)+9)).earliest('Day')
			LastQtr_SP_Ind = Index_SP500.objects.filter(Day=p.Day)
			posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(LastQtr_SP_Ind))
			return render(request, 'blog/SP_LastQtr.html', {'SP_LastQtr_posts': posts})
		except ObjectDoesNotExist:
			return render(request, 'blog/NoPeriod_SP.html')

def DJ_Last6Mnth(request):  #Display value from the 1st (trading) day of last quarter.
	p = Index_DJ.objects.latest('Day')
	LastDay = datetime.datetime.strptime(str(p.Day),'%Y-%m-%d')
	CurrYr = LastDay.strftime('%Y')
	CurrMnth = LastDay.strftime('%m')
	if int(CurrMnth) >= 7:  #Check whether last quarter is still within the same year.
		try:
			p = Index_DJ.objects.filter(Day__year=CurrYr, Day__month=str(int(CurrMnth)-6)).earliest('Day')
			#print p.Day, type(p)#, p.count()
			Last6Mnth_DJ_Ind = Index_DJ.objects.filter(Day=p.Day)
			posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(Last6Mnth_DJ_Ind))
			#print posts.count()
			return render(request, 'blog/DJ_Last6Mnth.html', {'DJ_Last6Mnth_posts': posts})
		except ObjectDoesNotExist:
			return render(request, 'blog/NoPeriod.html')
	else:
		try:
			p = Index_DJ.objects.filter(Day__year=str(int(CurrYr)-1), Day__month=str(int(CurrMnth)+6)).earliest('Day')
			#print p.Day, type(p)#, p.count()
			Last6Mnth_DJ_Ind = Index_DJ.objects.filter(Day=p.Day)
			posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(Last6Mnth_DJ_Ind))
			#print posts.count()
			return render(request, 'blog/DJ_Last6Mnth.html', {'DJ_Last6Mnth_posts': posts})
		except ObjectDoesNotExist:
			return render(request, 'blog/NoPeriod.html')

def SP_Last6Mnth(request):
	p = Index_SP500.objects.latest('Day')
	LastDay = datetime.datetime.strptime(str(p.Day),'%Y-%m-%d')
	CurrYr = LastDay.strftime('%Y')
	CurrMnth = LastDay.strftime('%m')
	if int(CurrMnth) >= 7:
		try:
			p = Index_SP500.objects.filter(Day__year=CurrYr, Day__month=str(int(CurrMnth)-6)).earliest('Day')
			Last6Mnth_SP_Ind = Index_SP500.objects.filter(Day=p.Day)
			posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(Last6Mnth_SP_Ind))
			#print posts.count()
			return render(request, 'blog/SP_Last6Mnth.html', {'SP_Last6Mnth_posts': posts})
		except ObjectDoesNotExist:
			return render(request, 'blog/NoPeriod_SP.html')
	else:
		try:
			p = Index_SP500.objects.filter(Day__year=str(int(CurrYr)-1), Day__month=str(int(CurrMnth)+6)).earliest('Day')
			Last6Mnth_SP_Ind = Index_SP500.objects.filter(Day=p.Day)
			posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(Last6Mnth_SP_Ind))
			return render(request, 'blog/SP_Last6Mnth.html', {'SP_Last6Mnth_posts': posts})
		except ObjectDoesNotExist:
			return render(request, 'blog/NoPeriod_SP.html')

def DJ_LastYr(request):  #Display value from the 1st (trading) day of last year.
	p = Index_DJ.objects.latest('Day')
	LastDay = datetime.datetime.strptime(str(p.Day),'%Y-%m-%d')
	CurrYr = LastDay.strftime('%Y')
	CurrMnth = LastDay.strftime('%m')
	try:
		p = Index_DJ.objects.filter(Day__year=str(int(CurrYr)-1), Day__month=CurrMnth).earliest('Day')  #Retrieve earliest date available from last year, doesn't matter the month.
		#print p.Day
		LastYr_DJ_Ind = Index_DJ.objects.filter(Day=p.Day)
		posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(LastYr_DJ_Ind))
		#print posts.count()
		if posts:
			return render(request, 'blog/DJ_LastYr.html', {'DJ_LastYr_posts': posts})
		else:
			return render(request, 'blog/NoPeriod.html') 
	except ObjectDoesNotExist:
		return render(request, 'blog/NoPeriod.html') 

def SP_LastYr(request):
	p = Index_SP500.objects.latest('Day')
	LastDay = datetime.datetime.strptime(str(p.Day),'%Y-%m-%d')
	CurrYr = LastDay.strftime('%Y')
	CurrMnth = LastDay.strftime('%m')
	try:
		p = Index_SP500.objects.filter(Day__year=str(int(CurrYr)-1), Day__month=CurrMnth).earliest('Day')
		LastYr_SP_Ind = Index_SP500.objects.filter(Day=p.Day)
		posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(LastYr_SP_Ind))
		if posts:
			return render(request, 'blog/SP_LastYr.html', {'SP_LastYr_posts': posts})
		else:
			return render(request, 'blog/NoPeriod_SP.html') 
	except ObjectDoesNotExist:
		return render(request, 'blog/NoPeriod_SP.html') 

def thanks(request):
	return render(request, 'blog/thanks.html')

def get_query(request):  #Implement logic for query search.
	master_list = all_ks.objects.all()  #master_list should be accessible at all lower nested levels to refine filter.
	q = request.GET.get("q")  #"q" is the name of query object in html (under input text).
	if not q:  #Check if user has entered a search term.
		#return HttpResponse('Please enter a search term')
		return render(request, 'blog/NoMatch.html')
	else:
		query = q.encode('utf-8').upper()  #Convert unicode string to regular (byte) string and uppercase to match database.
		#print "User query:", query, type(query), len(query)
		queryset_list = master_list.filter(Symbol__iexact=query)  #Apply 'iexact' lookuptype to find case-insensitive filter with EXACT match in a given field, "Symbol".
		SymList = queryset_list.values_list('Symbol', flat=True).order_by('Symbol')  #Retrieve only 'Symbol' field from queryset as a list for all symbols matching the query. If flat=True, results are returned as single values, rather than tuples.
		#print SymList, type(SymList)
		byte_list = [i.encode('utf-8') for i in SymList]  #Convert unicode to byte string for every item in the list.
		#print byte_list, type(byte_list)
		byte_list = list(set(byte_list))  #Eliminate redundancy in the list.
		#print "Symbol list from 'Symbol' field EXACTLY matching user query:", byte_list, type(byte_list), len(byte_list)
		if len(byte_list) == 1:  #One EXACT match is found in 'Symbol' field of the database.
			#return HttpResponse('One symbol found.')
			#print "One result found with EXACT match to user query:", byte_list, type(byte_list)
			last_element = queryset_list.last()  #Get the last entry in the queryset to display latest company name as table caption in html.
			return render(request, 'blog/results.html', {'posts': queryset_list, 'last_element': last_element})
		else:  #0 or more than 1 match is found in 'Symbol' field of the database.
			#print "Look for 'Symbol' CONTAINING user query."
			queryset_list = master_list.filter(Symbol__icontains=query)  #If no exact match of symbol search is found, apply 'icontains' lookuptype to apply case-insensitive filter with SUBSTRING match in a given field, "Symbol".
			#print queryset_list
			SymList = queryset_list.values_list('Symbol', flat=True).order_by('Symbol')
			byte_list = [i.encode('utf-8') for i in SymList]
			byte_list = list(set(byte_list))
			#print "'Symbol' CONTAINING user query:", byte_list, type(byte_list), len(byte_list)
			if len(byte_list) >= 1:  #At least one 'Symbol' in the database CONTAINS the query.
				#print "At least one 'Symbol(s)' CONTAINS user query:", byte_list, type(byte_list), len(byte_list)
				#print type(queryset_list)
				queryset_list = queryset_list.values('Symbol', 'Name').distinct()  #Use .values() to include all fields to display in results table; add .distinct() to retrieve all unique field combination; queryset_list is converted from QuerySet object to ValuesQuerySet object.
				#print queryset_list, type(queryset_list)
				return render(request, 'blog/NoMatch.html', {'posts': queryset_list})
			else:  #User query doesn't match any symbol in the database (exact or partial).
				#print "None of the 'Symbols' in the database matches user query. Try searching 'Name' field."
				queryset_list = master_list.filter(Name__icontains=query)  #If no exact or substring match is found in the "Symbol" field, check if query substring is CONTAINED within 'Name' field using 'icontains' (disregarding case).
				SymList = queryset_list.values_list('Symbol', flat=True).order_by('Symbol')
				byte_list = [i.encode('utf-8').upper() for i in SymList]
				byte_list = list(set(byte_list))
				#print "Symbol(s) found containing user query under 'Name' field:", byte_list, type(byte_list), len(byte_list)
				if len(byte_list) >= 1:  #At least one 'Name' in the database CONTAINS the query.
					#print type(queryset_list)
					queryset_list = queryset_list.values('Symbol', 'Name').distinct()
					#print queryset_list, type(queryset_list)
					return render(request, 'blog/NoMatch.html', {'posts': queryset_list})
				else:  #Try approximate matching of query string; assemble a unique word list from 'Name' field 1st.
					Name_words = master_list.values('Name').distinct()
					#print "Distinct 'Name' field:", Name_words, type(Name_words), len(Name_words)
					Name_words = Name_words.values_list('Name', flat=True).order_by('Symbol')  #Convert distionary ('Name' field only) to ValuesQuerySet format.
					Name_words = list(Name_words)  #Convert ValuesQuerySet to list format.
					#print "Converted to list:", Name_words, type(Name_words), len(Name_words)
					gssm = []  #Creat a list to get substring match from query.
					for unsplit in Name_words:  #Check if query is contained within the substring for each company name retrieved.
						#print unsplit
						for word in unsplit.split(' '):
							#print word
							gssm.append(word.replace('&APOS;',"'").replace('AMP;',"").replace('(','').replace(')','').upper())  #Separate words in 'Name' field and append to new list (in upper case).
					gssm = list(set(gssm))
					#print gssm, type(gssm), len(gssm)
					close_matches = get_close_matches(query, gssm)  #Only retrieve closest match (including matching cases).
					#print "Did you mean?", close_matches
					#return HttpResponse('Did you enter the right search term? Closest match: '+close_matches[0])
					return render(request, 'blog/NoMatch.html', {'posts': close_matches})

def AboutMe(request):  #In-Progress url
	return render(request, 'blog/AboutMe.html')

def contact_form(request):
	'''
	form_class = ContactForm  #use for email submission.
	'''
	if request.method == 'POST':
		form = ContactForm(request.POST)  #Accept user input as 'request.POST'; use form_class(request.POST) with email submission.
		if form.is_valid():  #runs validation checks for all fields and returns Boolean.
			obj = UserComment()  #Generate new UserComment object (see models.py).
			obj.name = form.cleaned_data['name']  #'cleaned_data' is used with 'is_valid' form method and normalizes input data to a consistent format.
			obj.email = form.cleaned_data['email']
			obj.message = form.cleaned_data['message']
			obj.save()  #Save the object to db.
			return render(request, 'blog/thanks.html')
	else:  #If a GET (such as first time the form is displayed), a blank form is created.
		form = ContactForm()
	return render(request, 'blog/contact.html', {'form': form})
	'''
			contact_name = request.POST.get('contact_name', '')
			contact_email = request.POST.get('contact_email', '')
			form_content = request.POST.get('content', '')
			template = get_template('blog/contact_template.txt')
			context = Context({'contact_name': contact_name, 'contact_email': contact_email, 'form_content': form_content,})
			content = template.render(context)
			email = EmailMessage("New contact form submission", content, "Fundamental Trader"+'', ['ericsun1221@gmail.com'], headers = {'Reply-To': contact_email })  #Must specify email inbox to send to.
			email.send()
			#return redirect('thanks.html')
			return render(request, 'blog/thanks.html')
	return render(request, 'blog/contact.html', {'form': form_class,})
	'''
