#To run, go to folder containing manage.py with the following command: >python manage.py [script name]from django.core.management.base import BaseCommand, CommandErrorimport csvimport requestsimport datetimeimport reimport randomimport time#from blog.models import DJ_indexclass Command(BaseCommand):	help = "Populates csv file for DJ index"	def handle(self, *args, **options):		today = str(datetime.date.today())		#print today		with open('DJ_index.csv', 'ab') as file:  #Use 'ab' to append in binary mode (preventing line skip) to existing csv file.			#file = open('DJ_index.csv', 'wb')			outfile = csv.writer(file, delimiter=",", quotechar='"')			response = requests.get('https://query1.finance.yahoo.com/v10/finance/quoteSummary/%5EDJI?formatted=true&crumb=vPC4QPS8MCo&lang=en-US&region=US&modules=components&corsDomain=finance.yahoo.com')			html = response.text  #Converts page request to string variable.			#print html			DJsym = ""			for ch in html.split('"components":[')[1]:				if ch != "]":					DJsym += ch				else:					break #Continue adding character ('ch') to 'DJsym' until '"' is ran into.			#print DJsym			pattern = re.compile('"(.+?)"')  #'.+' represents one-or-more-character string while '?' at the end represents non-greedy retrieval.			DJlist = pattern.findall(DJsym)  #Find all pattern in DJsym and return them as a list. Note: no need to predefine (DJlist=[]).			DJlist.sort()  #list.sort() method modifies the list in-place and is slightly more efficient than sorted(list).			print DJlist			for tick in DJlist:				outfile.writerow([today, tick])		'''		if DJlist:  #To avoid entering duplicate data, only enter into sql database if DJlist is neither empty nor null.			fields = ['Day', 'Symbol']  #Must match individual column names in models.py for entry into database.			with open('DJ_index.csv', 'rb') as file:  # May need to use absolute path when on Pythonanywhere server (i.e. use '/home/cqcum6er/my-first-blog/DJ_index.csv' as file path.)				infile = csv.reader(file, delimiter=",", quotechar='"')  #Specify csv item boundary.				LastRowDate = ""  #Reserve a variable for the date from last row .				#print type(LastRowDate)				for row in reversed(list(infile)):  #Read csv file in reverse order or the most recent entry 1st for display on server; must convert csv reader object to list format 1st with list().					if row[0] == LastRowDate or LastRowDate == "":  #Keep write to database while the date is still the same as last entry.						DJ_index.objects.create(**dict(zip(fields, row)))  #zip() combines two lists into one list of pairs of items from both lists (fields and row). dict() converts the list of pairs into a dictionary. (**{'key': 'value'}) is the equivalent of function(key='value').						LastRowDate = row[0]  #Mark the current date for comparison to the next date from the next row.					else:						break						'''