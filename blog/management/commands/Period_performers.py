#Save % price diff for different dates presented as options for user on the home menu as a database object (all_ks_DatePriceDiff) for quick access.
from django.core.management.base import BaseCommand, CommandError
#import csv
import datetime
from blog.models import all_ks, all_ks_DatePriceDiff

class Command(BaseCommand):
	help = "Asynchronous calculation of % price diff for diff dates from all_ks model object, & calcuation is done daily (format of model = date, company name, symbol, % price diff for yesterday, one week, & one month)."

	def handle(self, *args, **options):
		p = all_ks.objects.latest('Day')  #Returns an object instance (not iterable) from latest date; if latest() is empty, it works with attributes defined by 'class Meta' in models.py. Note latest () only retrieve ONE instance; .values() needs to be inserted in front of latest() to make it iterable as dictionary; cache queryset object for quick retrieval in html request.
		#print p, type(p)
		Latest_all_ks = all_ks.objects.filter(Day=p.Day)  #Return all index symbols from latest date.
		#print Latest_all_ks, type(Latest_all_ks)
		posts = all_ks.objects.filter(Day=p.Day, Symbol__in=list(Latest_all_ks))  #Filter with both conditions in paranthesis for AND operation instead of OR; use '__in=list()' format to retrieve all instance of DJ index.
		#Movers = []
		#print posts, type(posts)
		all_ks_DatePriceDiff.objects.all().delete()  #Remove all % price diff calculation from the previous date.
		for post in posts:  #for post in posts[400:]:
			if post.Day is None:  #Don't need to calculate % difference between different dates if today's date doesn't even exist.
				continue
			row = all_ks_DatePriceDiff.objects.create()  #Create an object instance to populate with.
			row.Day = post.Day  #Record date as the most current date of stock entry, not necessarily today's date; same as setattr(row, "Day", post.Day)
			row.Name = post.Name
			row.Symbol = post.Symbol
			print row.Symbol
			User_Date = {'Price_1': 1, 'Price_7': 7, 'Price_30': 30}
			for key, value in User_Date.iteritems():  #User_Date.items():
				Day_Delta = p.Day - datetime.timedelta(days=value)  #Get datetime for user specified range.
				#print Day_Delta
				#print key, type(key), value, type(value)
				try:
					ypost = all_ks.objects.filter(Day=Day_Delta, Symbol=post.Symbol)[0]  #Use .first() or '[0]' with filter to ensure only the first AND only entry in queryset is retrieved for the past date.
				except IndexError:  #Return None in case the list is empty.
					ypost = None
				#print post.Symbol, post.LastPrice, type(post.LastPrice), ypost.LastPrice, type(ypost.LastPrice),
				#if not ypost:  #Skip % diff calculation if a date doesn't exist. Note: "if not ypost.LastPrice:" OR "if type(ypost.LastPrice) is None:" doesn't work since ypost.LastPrice is an unicode object.
					#continue #Skip input for User_date if none exists.
				if (post is None) or (post.LastPrice == "N/A") or (ypost is None) or (ypost.LastPrice == "N/A"):  #Return "N/A" if no price is reported (or invalid) for today or user-specified date.
					print row, key, None
					setattr(row, key, None)  #row.key (object instance.field) syntax may not function in a for-loop; use None as null value for DecimalFields.
				else:
					PercDayMov = ((float(post.LastPrice) - float(ypost.LastPrice))/float(ypost.LastPrice))*100
					#print PercDayMov, type(PercDayMov)
					#row.key = str(PercDayMov)  #Convert to str format before saving to field of the model instance
					print row, key, str(PercDayMov)
					setattr(row, key, str(PercDayMov))
					#row.key = 'test'
					#print row.key, type(row.key)
					#row.save()
				
			row.save()  #Save all stats for each symbol before iterating to the next symbol.