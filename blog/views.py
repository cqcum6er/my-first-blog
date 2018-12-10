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
from .models import UserComment, Index_DJ, Index_SP500, all_ks, all_ks_DatePriceDiff  #Retrieve model objects from 'models.py' within the same folder.
from .forms import ContactForm, MoverForm, IndexForm
#from .templatetags import index_table
import datetime
import time
from django.db import connection  #Check sqlite connection speed with "connection.queries".
import csv
#import itertools

'''
#To update database with the current date, save scheduled csv record from Pythonanywhere (Export "all_ks" table as csv file [i.e.'all_ks_export.csv'] and save to the same directory as views.py), then run local server ONCE to populate local database before commenting out this block (may need to remove duplicate rows with sqlite command afterward); comment out this block before uploading views.py to Pythonanywhere to use scheduled csv instead...
import csv
#if not Post:  #Check to see if database is empty.  If it's not, do nothing, else empty existing entry to prepare for update. (Remove the 'if' statement if run as a scheduler command on Pythonanywhere.)
	#pass
#else:
	#all_ks.objects.all().delete()  #Clean the database before entry from csv file (If tables was dropped by SQL command, the table structure must be created 1st).
p = all_ks.objects.latest('Day')  #p = Post.objects.latest('Day')  #Check what's the lastest day then append to db from then on.
fields = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'FiftyTwoWkLo', 'FiftyTwoWkHi', 'DivYild', 'TrailPE', 'ForwardPE', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA', 'Name']  #Must match individual field (column) names in models.py.
with open('all_ks_export.csv', 'rb') as file:  # Export all_ks table as csv file ('all_ks_export.csv') and save to the same directory as views.py before upating; need to use absolute path when on Pythonanywhere server (i.e. use '/home/cqcum6er/my-first-blog/DJ_list.csv' as file path.)
	infile = csv.reader(file, delimiter=",", quotechar='"')  #Specify csv item boundary.
	for row in infile:
		row_datetime = datetime.datetime.strptime(row[0],'%Y-%m-%d')  #row[0] is converted from str to datetime format (i.e. '2017-08-27').
		#print row_datetime.date()
		row_date = row_datetime.date()  #Converting from datetime to date.
		if row_date > p.Day:  #Only append entry if the date of the entry is later than the most recent in db.
			#print row_date
			all_ks.objects.create(**dict(zip(fields, row)))
p = Index_DJ.objects.latest('Day')
fields = ['Symbol', 'Day',]
with open('blog_index_dj.csv', 'rb') as file:
	infile = csv.reader(file, delimiter=",", quotechar='"')
	for row in infile:
		row_datetime = datetime.datetime.strptime(row[2],'%Y-%m-%d')
		row_date = row_datetime.date()
		if row_date > p.Day:
			Index_DJ.objects.create(**dict(zip(fields, row)))
p = Index_SP500.objects.latest('Day')
fields = ['Day', 'Symbol']
with open('blog_index_SP500.csv', 'rb') as file:
	infile = csv.reader(file, delimiter=",", quotechar='"')
	for row in infile:
		row_datetime = datetime.datetime.strptime(row[0],'%Y-%m-%d')
		row_date = row_datetime.date()
		if row_date > p.Day:
			Index_SP500.objects.create(**dict(zip(fields, row)))
#...end of block.
'''

def Movers(Ind, User_Date, Dis_num):  #Sorts index components into top/bottom performers based during user-specified period; 'Ind' must be db object, & User_Date a string object.
	'''
	ts = time.time()  #Record current time; see <http://stackoverflow.com/questions/13890935/timestamp-python>
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')  #Convert current time to a readable format.
	print "Start time: "+st
	'''
	#Asynchronous calculation of % price diff based on user input; use stored % price diff as a model object that is refreshed daily (format of model = date, company name, symbol, % price diff for yesterday, one week, & one month); USE .order_by() DB OPERATION INSTEAD OF PYTHON .sort() TO SPEED UP ACCESS.
	p = Ind.objects.latest('Day')  #Returns an object instance (not iterable) from latest date; if latest() is empty, it works with attributes defined by 'class Meta' in models.py. Note latest () only retrieve ONE instance; .values() needs to be inserted in front of latest() to make it iterable as dictionary; cache queryset object for quick retrieval in html request.
	#print p, type(p)
	Latest_Ind = Ind.objects.filter(Day=p.Day)  #Return all index symbols from latest date.
	#print Latest_Ind, type(Latest_Ind)
	posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(Latest_Ind))  #Filter with both conditions in paranthesis for AND operation instead of OR; use '__in=list()' format to retrieve all symbol in the index.
	#print posts, type(posts)
	User_Date_dict = {'Price_1': 1, 'Price_7': 7, 'Price_30': 30}
	User_filter = [(key, val) for (key, val) in User_Date_dict.iteritems() if User_Date == val]  #List comprehension to determine user input; in Python 2.x .items() returns a list with tuple, not an iterator (.iteritems() is removed in Python 3.x).
	#print next(User_filter, None), type(next(User_filter, None))  #Retrieve the next item from the iterator. If default (2nd arg) is given, it is returned if the iterator is exhausted, otherwise StopIteration is raised.
	#print User_filter, type(User_filter)
	#print User_filter.next(), type(User_filter.next())
	#results = itertools.islice(User_filter, 0)
	#print results, type(results)
	key = User_filter[0][0]  #Return field with user-specified date within the tuple of the list.
	#key = next(User_filter, None)[0]
	#key = User_filter.next()[0]  #Get key from generator dict.
	#print key
	rev_key = '-' + key
	#val = User_filter.next()[1]  #Get val from generator dict.
	variable_column = key
	search_type = 'isnull'
	filter = variable_column + '__' + search_type  #Use kwarg 'filter' for variable column name for .exclude() (removing instance where the value is null for user-specified period).
	Top_disp = all_ks_DatePriceDiff.objects.filter(Symbol__in=list(Latest_Ind)).order_by(rev_key).values('Name', 'Symbol', key).exclude(**{ filter: True })[:Dis_num]  #Use .only() to select fields to display (for faster access, use .values() to return a list of dict instead of queryset object); .exclude() excludes instance where price for a date doesn't exist.
	#Top_disp = all_ks_DatePriceDiff.objects.filter(Symbol__in=list(Latest_Ind), key__icontains='').order_by(key)#[:Dis_num]
	#Top_disp = all_ks_DatePriceDiff.objects.extra(select={key: 'CAST(all_ks_DatePriceDiff.key AS INTEGER)'}, order_by=[key])
	#print Top_disp, type(Top_disp)
	Bottom_disp = all_ks_DatePriceDiff.objects.filter(Symbol__in=list(Latest_Ind)).order_by(key).values('Name', 'Symbol', key).exclude(**{ filter: True })[:Dis_num]
		
	'''
	for key, val in User_Date_dict.iteritems():  #In Python 2.x .items() returns a list with tuple, not an iterator (.iteritems() is removed in Python 3.x).
		if User_Date == val:
			Top_disp = all_ks_DatePriceDiff.objects.filter(Symbol__in=list(Latest_Ind)).exclude(key='').order_by(key)#[:Dis_num]
			#Top_disp = all_ks_DatePriceDiff.objects.filter(Symbol__in=list(Latest_Ind), key__icontains='').order_by(key)#[:Dis_num]
			#Top_disp = all_ks_DatePriceDiff.objects.extra(select={key: 'CAST(all_ks_DatePriceDiff.key AS INTEGER)'}, order_by=[key])
			#Bottom_disp = all_ks_DatePriceDiff.objects.filter(Symbol__in=list(Latest_Ind)).order_by(-key)[:Dis_num]
			#print type(Top_disp), type(Bottom_disp)
		else:
			continue  #Continue to check if user entered another date.
	'''
	'''
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	print "End time: "+st
	'''
	return (Top_disp, Bottom_disp, key)  #Return a tuple of top/bottom performers (as queryset instead of list to speed up access), accessible via Movers(...)[0] or Movers(...)[1].
	
	'''
	#Asynchronous calculation of % price diff based on user input; store % price diff as a model object that is refreshed daily (format of model = date, company name, symbol, % price diff for yesterday, one week, & one month).
	p = Ind.objects.latest('Day')  #Returns an object instance (not iterable) from latest date; if latest() is empty, it works with attributes defined by 'class Meta' in models.py. Note latest () only retrieve ONE instance; .values() needs to be inserted in front of latest() to make it iterable as dictionary; cache queryset object for quick retrieval in html request.
	#print p, type(p)
	Latest_Ind = Ind.objects.filter(Day=p.Day)  #Return all index symbols from latest date.
	#print Latest_Ind, type(Latest_Ind)
	posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(Latest_Ind))  #Filter with both conditions in paranthesis for AND operation instead of OR; use '__in=list()' format to retrieve all instance of DJ index.
	Movers = []
	#print posts, type(posts)
	User_Date_dict = {'Price_1': 1, 'Price_7': 7, 'Price_30': 30}
	for key, value in User_Date_dict.iteritems():
		if User_Date == value:
			for post in posts:
				all_ks_DPD = all_ks_DatePriceDiff.objects.filter(Symbol=post.Symbol).first()  #Select an instance (one company) from db object "all_ks_DatePriceDiff" if it is present in the latest index entry; use .first() to ensure only one instance is selected.
				#print all_ks_DPD, type(all_ks_DPD),
				if not all_ks_DPD:  #Skip to the next symbol for % diff calculation if an instance (one company) doesn't exist.
					continue
				if getattr(all_ks_DPD, key) == "N/A":  #all_ks_DPD.key may not function in a for-loop; skip to the next symbol for % diff calculation if no price is reported (or invalid) for user-specified date.
					continue  #Don't append to Movers list if the user-requested date doesn't exist; move on to the next instance (company).
					#Movers.append(tuple((all_ks_DPD.Symbol, all_ks_DPD.Name, '0')))
				else:
					Movers.append(tuple((all_ks_DPD.Symbol, all_ks_DPD.Name, float(getattr(all_ks_DPD, key)))))  #Add each symbol and it daily % movement as a tuple to a list ('Movers'); convert % price diff to float to sort correctly.
		else:
			continue  #Continue to check if user entered another date.
	Movers.sort(key=lambda tup: tup[2])  #Sort the tuple based on daily % movement (3rd element of each tuple entry) using the anonymous function, lambda.
	#print Movers, type(Movers)
	Top_disp = list(reversed(Movers[-Dis_num:]))  #'reversed' returns a 'listreverseiterator' type instead of a list type.
	Bottom_disp = Movers[:Dis_num]
	#print type(Top_disp), type(Bottom_disp)
	return (Top_disp, Bottom_disp)  #Return a tuple of top/bottom performers, accessible via Movers(...)[0] or Movers(...)[1].
	'''
	'''
	#Retrieve the results of % price diff for diff dates from a csv file for asynchronous operation (format of csv = date, company name, symbol, % price diff for yesterday, one week, & one month).
	with open('Period_performers.csv', 'rb') as file:
		infile = csv.reader(file, delimiter=",", quotechar='"')
		p = Ind.objects.latest('Day')  #Returns an object instance (a Symbol) from latest date.
		Latest_Ind = Ind.objects.filter(Day=p.Day)  #Return all index symbols from latest date.
		#print Latest_Ind, type(Latest_Ind)
		Mover_ind = []
		for row in list(infile):  #Convert csv reader object ("infile") to a list format before iteration.
			#print row[1], type(row[1])
			if Latest_Ind.filter(Symbol=row[2]).exists():  #Check if Symbol (row[2]) exists in queryset Latest_Ind.
				if User_Date == 1 and row[3]: #Check user-specified date & if % price diff (row[3]) exists for that date.
					#print row[2], row[3]
					Mover_ind.append(tuple((row[2], row[1], float(row[3]))))  #Add each symbol and it daily % movement as a tuple to a list ('Mover_ind').
				elif User_Date == 7 and row[4]:
					#print row[2], row[4]
					Mover_ind.append(tuple((row[2], row[1], float(row[4]))))
				elif User_Date == 30 and row[5]:
					#print row[2], row[5]
					Mover_ind.append(tuple((row[2], row[1], float(row[5]))))
				else:
					continue  #Skip to next symbol if % price diff doesn't exists.
			else:
				continue  #Skip to next symbol if none exists.
		Mover_ind.sort(key=lambda tup: tup[2])  #Sort the list of tuples based on % price diff between today and user-specified date; must convert from str to float for correct sorting.
		#print Mover_ind
		Top_disp = list(reversed(Mover_ind[-Dis_num:]))  #'reversed' returns a 'listreverseiterator' type instead of a list type.
		Bottom_disp = Mover_ind[:Dis_num]
		#print type(Top_disp), type(Bottom_disp)
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		print "End time: "+st
		return (Top_disp, Bottom_disp)  #Return a tuple of top/bottom performers, accessible via Movers(arg1,2,3)[0] or Movers(arg1,2,3)[1].
	'''
	'''
	#Synchronous calculation of % price diff based on user input.
	p = Ind.objects.latest('Day')  #Returns an object instance (not iterable) from latest date; if latest() is empty, it works with attributes defined by 'class Meta' in models.py. Note latest () only retrieve ONE instance; .values() needs to be inserted in front of latest() to make it iterable as dictionary; cache queryset object for quick retrieval in html request.
	#print p, type(p)
	Latest_Ind = Ind.objects.filter(Day=p.Day)  #Return all index symbols from latest date.
	#print Latest_Ind, type(Latest_Ind)
	posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(Latest_Ind))  #Filter with both conditions in paranthesis for AND operation instead of OR; use '__in=list()' format to retrieve all instance of DJ index.
	Day_Delta = p.Day - datetime.timedelta(days=User_Date)  #Get datetime for user specified range.
	Movers = []
	#print posts, type(posts)
	for post in posts:
		ypost = all_ks.objects.filter(Day=Day_Delta, Symbol=post.Symbol).first()  #Use .first() or '[0]' with filter to ensure only the first AND only entry in queryset is retrieved.
		#print post.Symbol, post.LastPrice, type(post.LastPrice), ypost.LastPrice, type(ypost.LastPrice),
		if not ypost:  #Skip % diff calculation if a date doesn't exist. Note: "if not ypost.LastPrice:" OR "if type(ypost.LastPrice) is None:" doesn't work since ypost.LastPrice is an unicode object.
			continue #break
		if post.LastPrice == "N/A" or ypost.LastPrice == "N/A":  #Return 0.0 if no price is reported (or invalid) today or user-specified date.
			PercDayMov = 0.0
		else:
			PercDayMov = ((float(post.LastPrice) - float(ypost.LastPrice))/float(ypost.LastPrice))*100
		#print PercDayMov
		Movers.append(tuple((post.Symbol, post.Name, PercDayMov)))  #Add each symbol and it daily % movement as a tuple to a list ('Movers').
	Movers.sort(key=lambda tup: tup[2])  #Sort the tuple based on daily % movement (3rd element of each tuple entry) using the anonymous function, lambda.
	#print Movers, type(Movers)
	Top_disp = list(reversed(Movers[-Dis_num:]))  #'reversed' returns a 'listreverseiterator' type instead of a list type.
	Bottom_disp = Movers[:Dis_num]
	#print type(Top_disp), type(Bottom_disp)
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	print "End time: "+st
	return (Top_disp, Bottom_disp)  #Return a tuple of top/bottom performers, accessible via Movers(...)[0] or Movers(...)[1].
	'''
	'''
	#Synchronous caculation of % price diff based on user input.
	#Ind = str(Ind)
	p = Ind.objects.latest('Day')  #Returns an object instance (not iterable) from latest date; if latest() is empty, it works with attributes defined by 'class Meta' in models.py. Note latest () only retrieve ONE instance; .values() needs to be inserted in front of latest() to make it iterable as dictionary; cache queryset object for quick retrieval in html request.
	Latest_Ind = Ind.objects.filter(Day=p.Day)  #Return all index symbols from latest date.
	posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(Latest_Ind))  #Filter with both conditions in paranthesis for AND operation instead of OR; use '__in=list()' format to retrieve all instance of DJ index.
	Day_Delta = p.Day - datetime.timedelta(days=User_Date)  #Get datetime for user specified range.
	Movers = []
	#print posts
	for post in posts:
		ypost = all_ks.objects.filter(Day=Day_Delta, Symbol=post.Symbol).first()  #Use .first() or '[0]' with filter to ensure only the first AND only entry in queryset is retrieved.
		#print post.Symbol, post.LastPrice, type(post.LastPrice), ypost.LastPrice, type(ypost.LastPrice),
		if not ypost:  #Skip % diff calculation if a date doesn't exist. Note: "if not ypost.LastPrice:" OR "if type(ypost.LastPrice) is None:" doesn't work since ypost.LastPrice is an unicode object.
			continue #break
		if post.LastPrice == "N/A" or ypost.LastPrice == "N/A":  #Return 0.0 if no price is reported (or invalid) today or user-specified date.
			PercDayMov = 0.0
		else:
			PercDayMov = ((float(post.LastPrice) - float(ypost.LastPrice))/float(ypost.LastPrice))*100
		#print PercDayMov
		Movers.append(tuple((post.Symbol, post.Name, PercDayMov)))  #Add each symbol and it daily % movement as a tuple to a list ('Movers').
	Movers.sort(key=lambda tup: tup[2])  #Sort the tuple based on daily % movement (3rd element of each tuple entry) using the anonymous function, lambda.
	#print Movers, type(Movers)
	Top_disp = list(reversed(Movers[-Dis_num:]))  #'reversed' returns a 'listreverseiterator' type instead of a list type.
	Bottom_disp = Movers[:Dis_num]
	#print type(Top_disp), type(Bottom_disp)
	return (Top_disp, Bottom_disp)  #Return a tuple of top/bottom performers, accessible via Movers(...)[0] or Movers(...)[1].
	'''
	'''
	p = Post.objects.latest('Day')  #Returns an object instance (not iterable); if latest() is empty, it works with attributes defined by 'class Meta' in models.py. Note latest () only retrieve ONE instance; .values() needs to be inserted in front of latest() to make it iterable as dictionary; cache queryset object for quick retrieval in html request.
	#print p.LastPrice, type(p.LastPrice)
	posts = Post.objects.filter(Day=p.Day)
	Yesterday = p.Day - datetime.timedelta(days=1)  #Get datetime for yesterday.
	Movers = []
	for post in posts:
		ypost = Post.objects.filter(Day=Yesterday).filter(Symbol=post.Symbol).first()  #Use .first() or '[0]' with filter to get the first entry in queryset, which always returns a single query.
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
	'''

def home(request):
	move_form = MoverForm()  #MoverForm(initial={'Ind_Mov': 'Index_DJ', 'Period_Mov': '1' 'Dis_num': '5'})  #Load empty form when the page is loaded the 1st time without user input; needed to initiate multiple forms on one page before checking user submission for each form.
	ind_form = IndexForm()
	Ind_Mov_label = "Dow Jones"  #Populate the initial empty form with default values; must be visible to the context dict.
	Period_Mov_label = "One Day"
	Ind = Index_DJ
	Period_Mov_val = 1
	Dis_num = 5
	Ind_Date_label = "Trading Day"
	'''
	if request.method == "GET":  #("perform_sub" in request.GET) or ("index_sub" in request.GET): #For single form in one page, use request.method == "GET" for condition test; for multiple forms in one page, check if the name of the submit button is included in the user QueryDict.
		#print request.GET, type(request.GET)
		submitted = request.GET.get('form_id', '')
		if submitted == 'perform_sub':
			move_form = MoverForm(request.GET)
			#print form, type(form)
			if move_form.is_valid():
				Ind_Mov = move_form.cleaned_data['Ind_Mov']  #Retrieve cleaned data (value) of 'Ind_Mov' selection in home.html (only usable after validation).
				#Ind_Mov = request.GET.get('Ind_Mov')
				#Ind_Mov = str(Ind_Mov)
				print Ind_Mov, type(Ind_Mov)  #Show cleaned user index selection.
				Ind_Mov_label = dict(move_form.fields['Ind_Mov'].choices).get(str(Ind_Mov))  #Get label (not key) of chosen ChoiceField.
				print Ind_Mov_label, type(Ind_Mov_label)  #Show user index selection as label.
				Period_Mov_val = move_form.cleaned_data['Period_Mov']  #Retrieve cleaned data (value) of 'Period_Mov'  selection in home.html.
				#Period_Mov = request.GET.get('Period_Mov')
				Period_Mov_val = int(Period_Mov_val)
				#print Period_Mov_val, type(Period_Mov_val)
				Period_Mov_label = dict(move_form.fields['Period_Mov'].choices).get(str(Period_Mov_val))  #Get label (not value or key) of chosen ChoiceField to display in template (applicable to form object).
				print Period_Mov_label, type(Period_Mov_label)  #Show user period selection for form display.
				Dis_num = move_form.cleaned_data['Dis_num']
				Dis_num = int(Dis_num)
				#print Dis_num, type(Dis_num)
				Performer_Index = str(Ind_Mov_label)  #Get the index title for output table.
				Performer_Period = str(Period_Mov_label)  #Get the period title for output table.
				if Ind_Mov_label == "Dow Jones":
					Ind = Index_DJ
				elif Ind_Mov_label == "S&P500":
					Ind = Index_SP500
		elif submitted == 'index_sub':
			ind_form = IndexForm(request.GET)
			if ind_form.is_valid():
				Ind_Date = ind_form.cleaned_data['Ind_Date']
				print Ind_Date, type(Ind_Date)  #Show user submission key.
				Ind_Date_label = dict(ind_form.fields['Ind_Date'].choices).get(str(Ind_Date))  #Get label (not key) of chosen ChoiceField.
				print Ind_Date_label, type(Ind_Date_label)  #Show user submission label.
	#else:
		#move_form = MoverForm()
		#ind_form = IndexForm()
	'''
	if request.method == "GET":  #("perform_sub" in request.GET) or ("index_sub" in request.GET): #For single form in one page, use request.method == "GET" for condition test; for multiple forms in one page, check if the name of the submit button is included in the user QueryDict.
		#print request.GET, type(request.GET)
		move_form = MoverForm(request.GET)
		ind_form = IndexForm(request.GET)
		#move_form_valid = move_form.is_valid()
		#ind_form_valid = ind_form.is_valid()
		if move_form.is_valid() and ind_form.is_valid():  #move_form_valid and ind_form_valid:
			#print form, type(form)
			Ind_Mov = move_form.cleaned_data['Ind_Mov']  #Retrieve cleaned data (value) of 'Ind_Mov' selection in home.html (only usable after validation).
			#Ind_Mov = request.GET.get('Ind_Mov')
			#Ind_Mov = str(Ind_Mov)
			#print Ind_Mov, type(Ind_Mov)  #Show cleaned user index selection.
			Ind_Mov_label = dict(move_form.fields['Ind_Mov'].choices).get(str(Ind_Mov))  #Get label (not key) of selected ChoiceField.
			#print Ind_Mov_label, type(Ind_Mov_label)  #Show user index selection as label.
			Period_Mov_val = move_form.cleaned_data['Period_Mov']  #Retrieve cleaned data (value) of 'Period_Mov'  selection in home.html.
			#Period_Mov = request.GET.get('Period_Mov')
			Period_Mov_val = int(Period_Mov_val)
			#print Period_Mov_val, type(Period_Mov_val)
			Period_Mov_label = dict(move_form.fields['Period_Mov'].choices).get(str(Period_Mov_val))  #Get label (not value or key) of chosen ChoiceField to display in template (applicable to form object).
			#print Period_Mov_label, type(Period_Mov_label)  #Show user period selection for form display.
			Dis_num = move_form.cleaned_data['Dis_num']
			Dis_num = int(Dis_num)
			#print Dis_num, type(Dis_num)
			#Performer_Index = str(Ind_Mov_label)  #Get the index title for output table.
			#Performer_Period = str(Period_Mov_label)  #Get the period title for output table.
			if Ind_Mov_label == "Dow Jones":
				Ind = Index_DJ
			elif Ind_Mov_label == "S&P500":
				Ind = Index_SP500

			Ind_Date = ind_form.cleaned_data['Ind_Date']
			#print Ind_Date, type(Ind_Date)  #Show user submission key.
			Ind_Date_label = dict(ind_form.fields['Ind_Date'].choices).get(str(Ind_Date))  #Get label (not key) of chosen ChoiceField.
			#print Ind_Date_label, type(Ind_Date_label)  #Show user submission label.
	'''
	if "perform_sub" in request.GET:  #For single form in one page, use request.method == "GET" for condition test; for multiple forms in one page, check if the name of the submit button is included in the user QueryDict.
		#print request.GET, type(request.GET)
		move_form = MoverForm(request.GET)
		#ind_form = IndexForm(request.GET)
		if move_form.is_valid():
			#print form, type(form)
			Ind_Mov = move_form.cleaned_data['Ind_Mov']  #Retrieve cleaned data (value) of 'Ind_Mov' selection in home.html (only usable after validation).
			#Ind_Mov = request.GET.get('Ind_Mov')
			#Ind_Mov = str(Ind_Mov)
			print Ind_Mov, type(Ind_Mov)  #Show cleaned user index selection.
			Ind_Mov_label = dict(move_form.fields['Ind_Mov'].choices).get(str(Ind_Mov))  #Get label (not key) of chosen ChoiceField.
			print Ind_Mov_label, type(Ind_Mov_label)  #Show user index selection as label.
			Period_Mov_val = move_form.cleaned_data['Period_Mov']  #Retrieve cleaned data (value) of 'Period_Mov'  selection in home.html.
			#Period_Mov = request.GET.get('Period_Mov')
			Period_Mov_val = int(Period_Mov_val)
			#print Period_Mov_val, type(Period_Mov_val)
			Period_Mov_label = dict(move_form.fields['Period_Mov'].choices).get(str(Period_Mov_val))  #Get label (not value or key) of chosen ChoiceField to display in template (applicable to form object).
			print Period_Mov_label, type(Period_Mov_label)  #Show label from user period selection dict for form display.
			Dis_num = move_form.cleaned_data['Dis_num']
			Dis_num = int(Dis_num)
			#print Dis_num, type(Dis_num)
			Performer_Index = str(Ind_Mov_label)  #Get the index title for output table.
			Performer_Period = str(Period_Mov_label)  #Get the period title for output table.
			if Ind_Mov_label == "Dow Jones":
				Ind = Index_DJ
			elif Ind_Mov_label == "S&P500":
				Ind = Index_SP500
	elif "index_sub" in request.GET:
		ind_form = IndexForm(request.GET)
		#move_form = MoverForm(request.GET)
		if ind_form.is_valid():
			Ind_Date = ind_form.cleaned_data['Ind_Date']
			print Ind_Date, type(Ind_Date)  #Show key from user submission dict.
			Ind_Date_label = dict(ind_form.fields['Ind_Date'].choices).get(str(Ind_Date))  #Get label (not key) of chosen ChoiceField.
			print Ind_Date_label, type(Ind_Date_label)  #Show label from user submission dict.
			Index_Sum = Ind_Date_label
	'''
	return render(request, 'blog/home.html', {
	'ind_form': ind_form,
	'move_form': move_form,
	'TopMovers': Movers(Ind, Period_Mov_val, Dis_num)[0],  #Collect 1st part of tuple as top movers.
	'BottomMovers': Movers(Ind, Period_Mov_val, Dis_num)[1],  #Collect 2nd part of tuple as bottom movers.
	'key': Movers(Ind, Period_Mov_val, Dis_num)[2],  #Collect 3rd part of tuple for custom dict filter.
	'Performer_Index': Ind_Mov_label,  #Flavor text for title.
	'Performer_Period': Period_Mov_label,  #Flavor text for title.
	'Index_Sum':Ind_Date_label
	})
	#Movers(Ind, Period_Mov_val, Dis_num)
	#return render(request, 'blog/home.html', {'ind_form': ind_form, 'form': form, 'TopMovers': Movers(Index_DJ, 1, 5)[0], 'BottomMovers': Movers(Index_DJ, 1, 5)[1],'Performer_Index':'Dow Jones', 'Performer_Period':'one day'})  #Load home page default values where there is no user input.
	#print connection.queries

def Ind_LastWk(request):
	form = MoverForm()
	return render(request, 'blog/Indices_LastWeek.html', {'form': form, 'TopMovers': Movers(Index_DJ, 1, 5)[0], 'BottomMovers': Movers(Index_DJ, 1, 5)[1],'Performer_Index':'Dow Jones', 'Performer_Period':'one day'})

def Ind_LastQtr(request):
	form = MoverForm()
	return render(request, 'blog/Indices_LastQuarter.html', {'form': form, 'TopMovers': Movers(Index_DJ, 1, 5)[0], 'BottomMovers': Movers(Index_DJ, 1, 5)[1],'Performer_Index':'Dow Jones', 'Performer_Period':'one day'})

def Ind_Last6Mnth(request):
	form = MoverForm()
	return render(request, 'blog/Indices_Last6Months.html', {'form': form, 'TopMovers': Movers(Index_DJ, 1, 5)[0], 'BottomMovers': Movers(Index_DJ, 1, 5)[1],'Performer_Index':'Dow Jones', 'Performer_Period':'one day'})

def Ind_LastYr(request):
	form = MoverForm()
	return render(request, 'blog/Indices_LastYear.html', {'form': form, 'TopMovers': Movers(Index_DJ, 1, 5)[0], 'BottomMovers': Movers(Index_DJ, 1, 5)[1],'Performer_Index':'Dow Jones', 'Performer_Period':'one day'})

def Ind_Last5Yr(request):
	form = MoverForm()
	return render(request, 'blog/Indices_Last5Years.html', {'form': form, 'TopMovers': Movers(Index_DJ, 1, 5)[0], 'BottomMovers': Movers(Index_DJ, 1, 5)[1],'Performer_Index':'Dow Jones', 'Performer_Period':'one day'})

def ResCenter_Def(request):
	return render(request, 'blog/ResCenter_Def.html')

def	ResCenter_Links(request):
	return render(request, 'blog/ResCenter_Links.html')

def	ResCenter_Plugs(request):
	return render(request, 'blog/ResCenter_Plugs.html')

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
		Latest_SP_Ind = Index_SP500.objects.filter(Day=p.Day)
		posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(Latest_SP_Ind))
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
	q = request.GET.get('q')  #Get raw query object "q" (NAME of input text) from html.
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
	if request.method == "POST":
		form = ContactForm(request.POST)  #Populate the form with 'request.POST' aka "binding data to the form" (ContactForm is a form object in forms.py).
		if form.is_valid():  #runs validation checks for all fields entered by user; if user input is invalid, user input is still kept on the current page for further user editing.
			obj = UserComment()  #Generate new UserComment object instance (see models.py).
			obj.name = form.cleaned_data['name']  #'cleaned_data' is used after confirmation with 'is_valid' form method and normalizes input data to a consistent format. Use "form.cleaned_data.get('name', 'default')" if a none value is expected ('deafult' will be printed in the case on none value).
			obj.email = form.cleaned_data['email']
			obj.message = form.cleaned_data['message']
			#obj.created_at = form.cleaned_data['message']
			obj.save()  #Save the object to db.
			return render(request, 'blog/thanks.html')
	else:  #If the user did not input any value or if the form is accessed for the 1st time , a blank form is created.
		form = ContactForm()
	return render(request, 'blog/contact.html', {'form': form})  #Render contact page before any user input. 
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