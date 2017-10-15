#To run, go to folder containing manage.py with the following command: >python manage.py [script name]#Make a csv file of SP500 tickers from most recent date and write them to database.from django.core.management.base import BaseCommand, CommandErrorimport csvimport requestsimport datetimeimport reimport randomimport timefrom blog.models import Index_SP500class Command(BaseCommand):	help = "Populates csv file for S&P500 index"	def handle(self, *args, **options):		today = str(datetime.date.today())		#print today		with open('index_SP500.csv', 'rb') as file:			infile = csv.reader(file, delimiter=",", quotechar='"')			LastDay = list(infile)[-1][0]  #Read the date for the most recent ticker entry.			#print LastDay, type(LastDay), today			if LastDay != today:  #Only append if today's tickers havn't already been entered into database.				with open('index_SP500.csv', 'ab') as file:  #Use 'ab' to append in binary mode (preventing line skip) to existing csv file.					#file = open('index_SP500.csv', 'wb')					outfile = csv.writer(file, delimiter=",", quotechar='"')					response = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')					html = response.text  #Converts page request to string variable.					#print html					SP500_list = []					for iter in xrange(1,html.count('XNYS:')+1):  #html.count() returns the number of (non-overlapping) occurrences of substring 'XNYS:'in html. xrange creats a list starting at 1 in this case.						SP500sym = ""						for ch in html.split('XNYS:')[iter]:							if ch != "\"":								SP500sym += ch							else:								break						SP500_list.append(SP500sym)					for iter in xrange(1,html.count('symbol/')+1):  #html.count() returns the number of (non-overlapping) occurrences of substring 'XNYS:'in html. xrange creats a list starting at 1 in this case.						SP500sym = ""						for ch in html.split('symbol/')[iter]:							if ch != "\"":								SP500sym += ch							else:								break						SP500_list.append(SP500sym)					SP500_list = [t.replace('.','-').replace('/','-').upper() for t in SP500_list]					SP500_list = sorted(SP500_list)					print SP500_list					for tick in SP500_list:						outfile.writerow([today, tick])			else:  #Don't append to csv file if last day in the file is the same as today.				pass		fields = ['Day', 'Symbol']  #Must match individual column names in models.py for entry into database.		#if SP500_list:  #To avoid entering duplicate data, only enter into sql database if SP500_list is neither empty nor null.		if Index_SP500.objects.exists():  #To avoid entering duplicate data, only enter into sql database if Index_SP500 is neither empty nor null.			LastEntry = Index_SP500.objects.latest('Day')			#print LastEntry.Day, type(str(LastEntry.Day)), type(today)			if str(LastEntry.Day) != today:  #Even if there is already data in database, the latest entry must not be from today to avoid duplicate entry from local update.				with open('index_SP500.csv', 'rb') as file:  # May need to use absolute path when on Pythonanywhere server (i.e. use '/home/cqcum6er/my-first-blog/index_SP500.csv' as file path.)					infile = csv.reader(file, delimiter=",", quotechar='"')  #Specify csv item boundary.					LastRowDate = ""  #Reserve a variable for the date from last row .					#print type(LastRowDate)					for row in infile:  #Read csv file in reverse order or the most recent entry 1st for display on server; must convert csv reader object to list format 1st with list().						#print row						if row[0] == LastRowDate or LastRowDate == "":  #Keep write to database while the date is still the same as last entry.							Index_SP500.objects.create(**dict(zip(fields, row)))  #zip() combines two lists into one list of pairs of items from both lists (fields and row). dict() converts the list of pairs into a dictionary. (**{'key': 'value'}) is the equivalent of function(key='value').							LastRowDate = row[0]  #Mark the current date for comparison to the next date from the next row.						else:							break		else:			with open('index_SP500.csv', 'rb') as file:				infile = csv.reader(file, delimiter=",", quotechar='"')				for row in infile:					Index_SP500.objects.create(**dict(zip(fields, row)))