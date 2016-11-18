from django.shortcuts import render
from .models import Post  #'Post' table object is retrieved from 'models.py' within the same folder.
import requests
import csv
import datetime

#Modify and move to write_csv once saved to Pythonanywhere to use scheduled csv...
if Post:  #Check to see if there is existing entry in database.  If there is, empty existing entry to prepare for update. (Remove the if statement for Pythonanywhere.)
	Post.objects.all().delete()
else:
	pass
fields = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'FiftyTwoWkLo', 'FiftyTwoWkHi', 'DivYild', 'TrailPE', 'ForwardPE', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA', 'Name']  #Must match individual field (column) names in models.py.
with open('DJ_list.csv', 'rb') as file:  # Need to use absolute path when on Pythonanywhere server (i.e. use '/home/cqcum6er/my-first-blog/DJ_list.csv' as file path.)
	infile = csv.reader(file, delimiter=",", quotechar='"')  #Specify csv item boundary.
	for row in infile:
		Post.objects.create(**dict(zip(fields, row)))  #zip() combines two lists into one list of pairs of items from both lists (fields and row). dict() converts the list of pairs into a dictionary. (**{'key': 'value'}) is the equivalent of function(key='value').
#...end of section for moving to write_csv.

def home(request):  #Home url
	return render(request, 'blog/home.html')

def inProgrss(request):  #In-Progress url
	return render(request, 'blog/InProgress.html')

def DJ_LastDay(request):  #"DJ_LastDay" must be requested from urls.py
		'''now = datetime.datetime.now()
		print type(now)
		print now
		posts = Post.objects.filter(Day__lte=now).last()#.values()'''
		'''first_date = datetime.date(2016, 9, 16)
		last_date = datetime.date(2016, 9, 17)
		posts = Post.objects.filter(Day__range=(first_date, last_date))'''
		posts = Post.objects.filter(Day__lte=datetime.date.today()).order_by('-Day')[:30]  #Retrieve the last 30 entry (as ordered by '-Day', which starts with the latest day) in db as QuerySet object (iterable).
		#posts = Post.objects.values()  #values() returns content of database as dictionary rather than model instances, thus making the database iterable.
		'''posts = Post.objects.values().latest('Day')  #If latest() is empty, it works with attributes defined by 'class Meta' in models.py. Note latest () only retrieve ONE instance.'''
		print type(posts)
		print posts
		return render(request, 'blog/DJ_LastDay.html', {'posts': posts})
'''
	with open('DJ_list.csv', 'rb') as file:  # Need to use absolute path when on Pythonanywhere server (i.e. use '/home/cqcum6er/my-first-blog/DJ_list.csv' as file path.)
		infile = csv.reader(file, delimiter=",", quotechar='"')
		#next(infile, None)  #Skip column headers.
		print type(infile)

		last_date = ""
		for row in reversed(list(infile)):  #Read csv file in reverse order (must convert csv reader object to list format 1st.)
			#if row.line_num == 1:
				#continue  #Skip column header; not needed with csv.reader?.
			todayTag = row[0]
			current_date = datetime.datetime.strptime(todayTag,'%Y-%m-%d').date()  #Convert str to time format and extract content in the format of "yyyy-mm-dd".  Use .date() to request just the date.
			current_date = str(current_date)  #Convert 'datetime.date' object to string for comparison.
			print current_date, type(current_date)
			print last_date, type(last_date)
			if current_date == last_date or last_date == "":  #Faster processing if put 'last_date == ""' last since it's only processed at the beginning row; keep writing out key statistics until date changes from today.
				post = Post(
				Symbol=row[1],  #Skip 1st date column (row[0]).
				LastPrice=row[2],
				FiftyTwoWkChg=row[3],
				FiftyTwoWkLo=row[4],
				FiftyTwoWkHi=row[5],
				DivYild=row[6],
				TrailPE=row[7],
				ForwardPE=row[8],
				PEG_Ratio=row[9],
				PpS=row[10],
				PpB=row[11],
				Market_Cap=row[12],
				Free_Cash_Flow=row[13],
				Market_per_CashFlow=row[14],
				Enterprise_per_EBITDA=row[15],
				Name=row[16],
				)
				#post.save()  #Save each entry ('post') of database.
			else:
				break  #Exit the smallest 'for' loop.
			last_date = current_date  #Save the current
		posts = Post.objects.values()  #values() returns content of database as dictionary, thus making the database iterable.
		return render(request, 'blog/DJ_LastDay.html', {'posts': posts})  #To serve as a template, 'blog/DJ.html' has to be put in blog\template\blog\
		#The last parameter, which looks like this: {} is a place to integrate objects in models.py (posts) with html ('posts') in template folder.


def DJ_LastWk(request):  #"DJ_LastWk" must be requested from urls.py
	if Post:  #Check to see if there is existing entry.  If there is, delete existing entry to prepare for updated entry.
		Post.objects.all().delete()
	else:
		pass
	with open('DJ_list.csv', 'rb') as file:  # Need to use absolute path when on Pythonanywhere server (i.e. use '/home/cqcum6er/my-first-blog/DJ_list.csv' as file path.)
		infile = csv.reader(file, delimiter=",", quotechar='"')
		#next(infile, None)  #Skip column headers.
		print type(infile)
		#last_date = ""
		for row in reversed(list(infile)):  #Read csv file in reverse order (must convert csv reader object to list format 1st.)
			todayTag = row[0]
			current_date = datetime.datetime.strptime(todayTag,'%Y-%m-%d').date()  #Convert str to time format and extract content in the format of "yyyy-mm-dd".  Use .date() to request just the date.
			LastWk_date = current_date - datetime.timedelta(days=7)
			#current_date = str(current_date)  #Convert 'datetime.date' object to string for comparison.
			print current_date, type(current_date)
			print LastWk_date, type(LastWk_date)
			if current_date == last_date or last_date == "":  #Faster processing if put 'last_date == ""' last since it's only processed at the beginning row; keep writing out key statistics until date changes from today.
				post = Post(
				Symbol=row[1],  #Skip 1st date column (row[0]).
				LastPrice=row[2],
				FiftyTwoWkChg=row[3],
				FiftyTwoWkLo=row[4],
				FiftyTwoWkHi=row[5],
				DivYild=row[6],
				TrailPE=row[7],
				ForwardPE=row[8],
				PEG_Ratio=row[9],
				PpS=row[10],
				PpB=row[11],
				Market_Cap=row[12],
				Free_Cash_Flow=row[13],
				Market_per_CashFlow=row[14],
				Enterprise_per_EBITDA=row[15],
				Name=row[16],
				)
				post.save()  #Save each entry ('post') of database.
			else:
				break  #Exit the smallest 'for' loop.
			last_date = current_date  #Save the current
			print current_date
			print last_date
		posts = Post.objects.values()  #values() returns content of database as dictionary, thus making the database iterable.
		return render(request, 'blog/DJ_LastWk.html', {'posts': posts})  #To serve as a template, 'blog/DJ.html' has to be put in blog\template\blog\
		#The last parameter, which looks like this: {} is a place to integrate objects in models.py (posts) with html ('posts') in template folder.
'''