#views.py retrieves model instances from the database or instantiate a form (see feedback_form).
from django.shortcuts import render, redirect #get_object_or_404
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist  #Display in-app message when an instance isn't found.
from django.http import HttpResponse
'''
from django.db.models import Q  #Allow simultaneous search in different fields.
from difflib import get_close_matches  #Allow 'approximate' search.
#For email.
from django.core.mail import EmailMessage, send_mail
from django.template import Context
from django.template.loader import get_template
'''
from .models import Post, UserComment  #Retrieve model objects from 'models.py' within the same folder.
from .forms import FeedbackForm
import requests
import csv
import datetime
import aniso8601
'''
#To update database with the current date, save scheduled csv record from Pythonanywhere, then run local server ONCE to populate local database before commenting out this block; comment out this block before saving views.py to Pythonanywhere to use scheduled csv instead...
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
p = Post.objects.latest('Day')  #Returns an object instance (not iterable); if latest() is empty, it works with attributes defined by 'class Meta' in models.py. Note latest () only retrieve ONE instance; .values() needs to be inserted in front of latest() to make it iterable as dictionary; cache queryset object for quick retrieval in html request.
LastDay = datetime.datetime.strptime(str(p.Day),'%Y-%m-%d')  #Convert str to datetime object from datetime module.
print LastDay
CurrYr = LastDay.strftime('%Y')  #Retrieve current year as string from datetime object, LastDay.
CurrMnth = LastDay.strftime('%m')  #Retrieve current month as string from datetime object, LastDay.

def iso_to_gregorian(iso_year, iso_week, iso_day):  #Converts ISO week date format to Gregorian calendar date format.
	jan4 = datetime.date(iso_year, 1, 4)  #1st week ('Week 01') of new year always contains Jan 4th.
	start = jan4 - datetime.timedelta(days=jan4.isoweekday()-1)  #Get the year for ISO week date.
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
	posts = Post.objects.filter(Day=p.Day)  #Retrieve all instances with latest day ('p.Day') as QuerySet object.
	'''print type(p.Day)
	print p.Day'''
	'''TestDay = datetime.datetime.strptime('2017-01-06','%Y-%m-%d')
	print TestDay
	print iso_to_gregorian(TestDay.isocalendar()[0], TestDay.isocalendar()[1]-1, 3)'''
	#print (aniso8601)
	return render(request, 'blog/DJ_LastDay.html', {'LastDay_posts': posts})#, {'LastDay': p.Day})  #To serve as a template, 'blog/DJ.html' has to be put in blog\template\blog\
	#The last parameter, which looks like this: {} is a place to integrate objects in models.py (posts) with html ('posts') in template folder.

def DJ_LastWk(request):  #Display value from Wednesday of last week.
	print iso_to_gregorian(LastDay.isocalendar()[0], LastDay.isocalendar()[1]-1, 3)  #Show date from last Wednesday.
	posts = Post.objects.filter(Day=iso_to_gregorian(LastDay.isocalendar()[0], LastDay.isocalendar()[1]-1, 3))  #Retrieve all instances from last Wednesday.
	return render(request, 'blog/DJ_LastWk.html', {'LastWk_posts': posts})

def DJ_LastMnth(request):  #Display value from the 1st (trading) day of last month.
	if int(CurrMnth) >= 2:  #Check whether last month is still within the same year.
		p = Post.objects.filter(Day__year=CurrYr, Day__month=str(int(CurrMnth)-1)).earliest('Day')  #Retrieve earliest date available from last month.
		print p.Day
		posts = Post.objects.filter(Day=p.Day)
	else:
		p = Post.objects.filter(Day__year=str(int(CurrYr)-1), Day__month=str(int(CurrMnth)+11)).earliest('Day')
		print p.Day
		posts = Post.objects.filter(Day=p.Day)
	return render(request, 'blog/DJ_LastMnth.html', {'LastMnth_posts': posts})

def DJ_LastQtr(request):  #Display value from the 1st (trading) day of last quarter.
	if int(CurrMnth) >= 4:  #Check whether last quarter is still within the same year.
		p = Post.objects.filter(Day__year=CurrYr, Day__month=str(int(CurrMnth)-3)).earliest('Day')
		print p.Day
		posts = Post.objects.filter(Day=p.Day)
	else:
		p = Post.objects.filter(Day__year=str(int(CurrYr)-1), Day__month=str(int(CurrMnth)+9)).earliest('Day')
		print p.Day
		posts = Post.objects.filter(Day=p.Day)
	return render(request, 'blog/DJ_LastQtr.html', {'LastQtr_posts': posts})

def DJ_LastYr(request):  #Display value from the 1st (trading) day of last year.
	try:
		p = Post.objects.filter(Day__year=str(int(CurrYr)-1), Day__month=CurrMnth).earliest('Day')  #Retrieve earliest date available from last year, doesn't matter the month.
		print p.Day
		posts = Post.objects.filter(Day=p.Day)
		return render(request, 'blog/DJ_LastYr.html', {'LastYr_posts': posts})
	except ObjectDoesNotExist:
		print "No entry exists for this month from last year, please try an earlier date."
		#return redirect('/NoData/') 

def thanks(request):
	return render(request, 'blog/thanks.html')
	
def feedback_form(request):
	'''
	form_class = FeedbackForm  #use for email submission.
	'''
	if request.method == 'POST':
		form = FeedbackForm(request.POST)  #Accept user input as 'request.POST'; use form_class(request.POST) with email submission.
		if form.is_valid():  #runs validation checks for all fields and returns Boolean.
			obj = UserComment()  #Generate new UserComment object (see models.py).
			obj.name = form.cleaned_data['name']
			obj.email = form.cleaned_data['email']
			obj.message = form.cleaned_data['message']
			obj.save()  #Save the object to db.
			return render(request, 'blog/thanks.html')
	else:  #If a GET (such as first time the form is displayed), a blank form is created.
		form = FeedbackForm()
	return render(request, 'blog/feedback.html', {'form': form})
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
	return render(request, 'blog/feedback.html', {'form': form_class,})
	'''

def edu_center(request):
	return render(request, 'blog/EduCenter.html')
	
def get_query(request):  #Implement logic for query search.
	master_list = Post.objects.all()  #master_list should be accessible at all lower nested levels to refine filter.
	q = request.GET.get("q")  #"q" is the name of query object in html (under input text).
	if not q:  #Check if user has entered a search term.
		#return HttpResponse('Please enter a search term')
		return render(request, 'blog/NoMatch.html')
	else:
		query = q.encode('utf-8').upper()  #Convert unicode string to regular (byte) string and uppercase to match database.
		print "User query:", query, type(query), len(query)
		queryset_list = master_list.filter(Symbol__iexact=query)  #Apply 'iexact' lookuptype to find case-insensitive filter with EXACT match in a given field, "Symbol".
		SymList = queryset_list.values_list('Symbol', flat=True).order_by('Symbol')  #Retrieve only 'Symbol' field from queryset as a list. If flat=True, results are returned as single values, rather than tuples.
		#print SymList, type(SymList)
		byte_list = [i.encode('utf-8') for i in SymList]  #Convert unicode to byte string for every item in the list.
		#print byte_list, type(byte_list)
		byte_list = list(set(byte_list))  #Eliminate redundancy in the list.
		print "Symbol list from 'Symbol' field EXACTLY matching user query:", byte_list, type(byte_list), len(byte_list)
		if len(byte_list) == 1:  #One EXACT match is found in 'Symbol' field of the database.
			#return HttpResponse('One symbol found.')
			print "One result found with EXACT match to user query:", byte_list, type(byte_list)
			return render(request, 'blog/results.html', {'posts': queryset_list})
		else:  #0 or more than 1 match is found in 'Symbol' field of the database.
			print "Look for 'Symbol' CONTAINING user query."
			queryset_list = master_list.filter(Symbol__icontains=query)  #If no exact match of symbol search is found, apply 'icontains' lookuptype to apply case-insensitive filter with SUBSTRING match in a given field, "Symbol".
			#print queryset_list
			SymList = queryset_list.values_list('Symbol', flat=True).order_by('Symbol')
			byte_list = [i.encode('utf-8') for i in SymList]
			byte_list = list(set(byte_list))
			print "'Symbol' CONTAINING user query:", byte_list, type(byte_list), len(byte_list)
			if len(byte_list) >= 1:  #At least one 'Symbol' in the database CONTAINS the query.
				print "At least one 'Symbol(s)' CONTAINS user query:", byte_list, type(byte_list), len(byte_list)
				print type(queryset_list)
				queryset_list = queryset_list.values('Symbol', 'Name').distinct()  #Use .values() to include all fields to display in results table; add .distinct() to retrieve all unique field combination; queryset_list is converted from QuerySet object to ValuesQuerySet object.
				print queryset_list, type(queryset_list)
				return render(request, 'blog/NoMatch.html', {'posts': queryset_list})
			else:  #User query doesn't match any symbol in the database (exact or partial).
				print "None of the 'Symbols' in the database matches user query. Try searching 'Name' field."
				queryset_list = master_list.filter(Name__icontains=query)  #If no exact or substring match is found in the "Symbol" field, check if query substring is CONTAINED within 'Name' field using 'icontains' (disregarding case).
				SymList = queryset_list.values_list('Symbol', flat=True).order_by('Symbol')
				byte_list = [i.encode('utf-8').upper() for i in SymList]
				byte_list = list(set(byte_list))
				'''
				gssm =[]  #Creat a list to get substring match from query.
				for item in byte_list:  #Check if query is contained within the substring for each company name retrieved.
					#print item
					if query in item:
						#gssm += item
						gssm.append(item)  #Add item to the list if a company name contains user query.
				print gssm, type(gssm)
				'''
				print "Symbol(s) found containing user query under 'Name' field:", byte_list, type(byte_list), len(byte_list)
				'''
				if len(byte_list) == 1:
					print "One result contained within 'Name' field:", byte_list, type(byte_list)
					return render(request, 'blog/results.html', {'query': queryset_list})
				else:
				'''
				print type(queryset_list)
				queryset_list = queryset_list.values('Symbol', 'Name').distinct()
				print queryset_list, type(queryset_list)
				'''
				Name_words = master_list.values('Name').distinct()
				print Name_words, type(Name_words), len(Name_words)
				gssm =[]  #Creat a list to get substring match from query.
				for item in Name_words:  #Check if query is contained within the substring for each company name retrieved.
					#print item
					#if query in item:
						#gssm += item
					gssm.append(item)  #Add item to the list if a company name contains user query.
				print gssm, type(gssm), len(gssm)
				
				gcm = get_close_matches(query, Name_words)  #Only retrieve closest match (including matching cases).
				print "Did you mean?", gcm
				'''
				return render(request, 'blog/NoMatch.html', {'posts': queryset_list})
		'''
		if len(byte_list) >= 2:  #Offer suggestion if more than one match is found in database.
			pass
		elif len(byte_list) == 1:
			gcm = get_close_matches(query, byte_list, 1)  #Only retrieve closest match (including matching cases).
			print gcm, type(gcm)
			if gcm:  #Check if query matches any of get_close_matches hits.
				gcm = gcm[0]  #Get only the 1st item in the list as string.
				#print gcm, type(gcm)
				queryset_list = queryset_list.filter(Symbol__iexact=gcm)  #Retrieve all day entry for the exact matching symbol.
				print queryset_list, type(queryset_list)
				return render(request, 'blog/results.html', {'query': queryset_list})
			else:
				return HttpResponse('Please enter a closer match for a symbol or a name. Search suggestion:')

			if gssm:
				gssm = gssm[0]
				queryset_list = queryset_list.filter(Name__icontains=gssm)  #Retrieve all day entry for the matching name.
				return render(request, 'blog/results.html', {'query': queryset_list})
			else:
				return HttpResponse('Please enter a closer match for a company name. Search suggestion:')
		'''