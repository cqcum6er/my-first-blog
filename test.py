#Test whether new csv or model entry can be generated correctly by accessing database object:>python Period_performers.py
'''
import sys
sys.path.append('C:\Python27\djangogirls\mysite\blog')
from mysite import settings
from django.core.management import setup_environ
setup_environ(settings)
'''
import csv
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')  #Configure Python to access database object (from blog.models) outside of manage.py directory.
import datetime
from blog.models import all_ks, all_ks_DatePriceDiff

#def handle(self, *args, **options):
	#global html  #Makes html accessible to all functions (StrFet and handle).

'''
if __name__ == '__main__':
	#sys.path.insert(0, 'C:\Python27\djangogirls\mysite\blog')
	#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'C:\Python27\djangogirls\mysite\mysite')
	#django.setup()
	print "test"
'''
#def Movers(Ind, User_Date, Dis_num):  #Sorts index components into top/bottom performers based during user-specified period; 'Ind' must be db object, & User_Date a string object.

#Asynchronous calculation of % price diff for diff dates from all_ks model object, & calcuation is done daily (format of model = date, company name, symbol, % price diff for yesterday, one week, & one month).
p = all_ks.objects.latest('Day')  #Returns an object instance (not iterable) from latest date; if latest() is empty, it works with attributes defined by 'class Meta' in models.py. Note latest () only retrieve ONE instance; .values() needs to be inserted in front of latest() to make it iterable as dictionary; cache queryset object for quick retrieval in html request.
#print p, type(p)
Latest_all_ks = all_ks.objects.filter(Day=p.Day)  #Return all index symbols from latest date.
#print Latest_all_ks, type(Latest_all_ks)
posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(Latest_all_ks))  #Filter with both conditions in paranthesis for AND operation instead of OR; use '__in=list()' format to retrieve all instance of DJ index.
#Movers = []
#print posts, type(posts)
for post in posts:  #for post in posts[400:]:
	'''
	if post.Symbol == "AAPL":
		break  #Break out of posts for-loop before AAPL.
	'''
	if post.Day is None:  #Don't need to calculate % difference between different dates if today's date doesn't even exist.
		continue
	row = all_ks_DatePriceDiff.objects.create()  #Create an object instance to populate with.
	row.Day = post.Day  #Record date as the most current date of stock entry, not necessarily today's date; same as setattr(row, "Day", post.Day)
	row.Name = post.Name
	row.Symbol = post.Symbol
	print row.Symbol
	User_Date = {'Price_1': 1, 'Price_7': 7, 'Price_30': 30}
	'''
	row.Price_1 = 'test1'
	row.Price_7 = 'test2'
	row.Price_30 = 'test3'
	'''
	for key, value in User_Date.iteritems():  #User_Date.items():
		Day_Delta = p.Day - datetime.timedelta(days=value)  #Get datetime for user specified range.
		print Day_Delta
		#print key, type(key), value, type(value)
		ypost = all_ks.objects.filter(Day=Day_Delta, Symbol=post.Symbol).first()  #Use .first() or '[0]' with filter to ensure only the first AND only entry in queryset is retrieved for the past date.
		#print post.Symbol, post.LastPrice, type(post.LastPrice), ypost.LastPrice, type(ypost.LastPrice),
		#if not ypost:  #Skip % diff calculation if a date doesn't exist. Note: "if not ypost.LastPrice:" OR "if type(ypost.LastPrice) is None:" doesn't work since ypost.LastPrice is an unicode object.
			#continue #Skip input for User_date if none exists.
		
		if (post is None) or (post.LastPrice == "N/A") or (ypost is None) or ypost.LastPrice == "N/A":  #Return "N/A" if no price is reported (or invalid) for today or user-specified date.
			setattr(row, key, 'N/A')
		else:
		
			PercDayMov = ((float(post.LastPrice) - float(ypost.LastPrice))/float(ypost.LastPrice))*100
			#print PercDayMov, type(PercDayMov)
			#row.key = str(PercDayMov)  #Convert to str format before saving to field of the model instance
			setattr(row, key, str(PercDayMov))
			#row.key = 'test'
			#print row.key, type(row.key)
			#row.save()
		
	row.save()  #Save all stats for each symbol before iterating to the next symbol.

'''
#Calculate % price diff for diff dates from all_ks model object to create a csv file for asynchronous operation (format of csv = date, company name, symbol, % price diff for yesterday, one week, & one month).
with open('Period_performers.csv', 'wb') as file:  #Use 'wb' to write in binary mode to existing csv file and replace whole content each time the operation is executed.
	#outfile = csv.writer(file, delimiter=",", quotechar='"')
	p = all_ks.objects.latest('Day')  #Returns an object instance (not iterable) from latest date; if latest() is empty, it works with attributes defined by 'class Meta' in models.py. Note latest () only retrieve ONE instance; .values() needs to be inserted in front of latest() to make it iterable as dictionary; cache queryset object for quick retrieval in html request.
	Latest_Ind = all_ks.objects.filter(Day=p.Day)  #Return all index symbols from latest date.
	posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(Latest_Ind))  #Filter with both conditions in paranthesis for AND operation instead of OR; use '__in=list()' format to retrieve all instance of DJ index from latest date.
	
	User_Date = [1, 7, 30]
	#Movers = []
	#print posts
	for post in posts:
		print post, type(post)
		file.write(str(post.Day)+','+str(post.Name.encode('utf-8'))+','+str(post.Symbol)+',')
		if post.Day is None:  #Don't need to calculate % difference between different dates if today's date doesn't exist.
			continue
		for date in User_Date:
			Day_Delta = p.Day - datetime.timedelta(days=date)  #Get datetime for user specified range.
			print Day_Delta
			ypost = all_ks.objects.filter(Day=Day_Delta, Symbol=post.Symbol).first()  #Use .first() or '[0]' with filter to ensure only the first AND only entry in queryset is retrieved to avoid error.
			#print post.Symbol, post.LastPrice, type(post.LastPrice), ypost.LastPrice, type(ypost.LastPrice),
			#if (post.LastPrice.filter().exists()) or (ypost.LastPrice.filter().exists()):
			#print type(post.LastPrice)
			#if (post.LastPrice) or (ypost.LastPrice):
			print type(ypost) #print type(post.LastPrice)
			if not ypost:  #Skip % diff calculation if a date doesn't exist. Note: "if not ypost.LastPrice:" OR "if type(ypost.LastPrice) is None:" doesn't work since ypost.LastPrice is an unicode object.
				continue #break
			if (post.LastPrice == "N/A") or (ypost.LastPrice == "N/A"):
			#Return 0.0 if no price is reported (or invalid) for today or user-specified date.
				PercDayMov = 0.0
			else:
				PercDayMov = ((float(post.LastPrice) - float(ypost.LastPrice))/float(ypost.LastPrice))*100  #Calculate price difference for each ticker for a user-specified date.
			#print PercDayMov
			#Movers.append(tuple((post.Symbol, post.Name, PercDayMov)))  #Add each symbol and it daily % movement as a tuple to a list ('Movers').
			file.write(str(PercDayMov)+',')
		file.write('\n')
'''
'''
filenames = ['index_DJ.csv'] #, 'index_SP500.csv']  #List all files to append to outfile.
with open('index_LastCombo.csv', 'wb') as outfile:  #Combine all indices from the most recent date.
	outfile = csv.writer(outfile, delimiter=",", quotechar='"')
	#print type(outfile)
	for fname in filenames:  #Iterate thru DJ and SP500 index csv.
		with open(fname) as infile:  #Read the content of each fname as infile.
			infile = csv.reader(infile, delimiter=",", quotechar='"')
			LastRowDate = ""  #Reserve a variable for the date from last row.
			for row in reversed(list(infile)):  #Read from last day of each index.
				if row[0] == LastRowDate or LastRowDate == "":  #Keep writing to database until the date changes.
					#print row
					outfile.writerow(row)
					LastRowDate = row[0]  #Update the current date for comparison to the next date in the next row.
				else:
					break
'''