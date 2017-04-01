#To run, go to folder containing manage.py with the following command: >python manage.py [script name]from django.core.management.base import BaseCommand, CommandErrorimport csvimport requestsimport datetimeimport reimport randomimport timefrom blog.models import Postclass Command(BaseCommand):	help = "Populates csv file for DJ list"	html = ""  #Makes html accessible to all functions (StrFet and handle).	def StrFet(self, sep, num, end):  #StrFet() function fetches components of key statistics page; att=attribute, sep=separator, num=Nth separator, end=delimiter.		if sep not in html:  #Return "N/A" when there is nothing inside {}.			return "N/A"		else:			att = ""			for ch in html.split(sep)[num]:				if ch != end:					att += ch				else:					break #terminates the nearest enclosing loop when '<' is ran into (the loop control target, ch, keeps its current value).			if att[0] == '"':  #Return "N/A" if raw is string.				return "N/A"			else:				return att	def handle(self, *args, **options):		today = str(datetime.date.today())		#print today		with open('DJ_list.csv', 'ab') as file:  #Use 'ab' to append in binary mode (preventing line skip) to existing csv file.			#file = open('DJ_list.csv', 'wb')			time.sleep(random.randint(0,10))			outfile = csv.writer(file, delimiter=",", quotechar='"')			response = requests.get('https://query1.finance.yahoo.com/v10/finance/quoteSummary/%5EDJI?formatted=true&crumb=vPC4QPS8MCo&lang=en-US&region=US&modules=components&corsDomain=finance.yahoo.com')			html = response.text  #Converts page request to string variable.			DJlist = []			DJsym = self.StrFet('"components":[', 1, "]")			'''			for iter in xrange(4,34):				DJsym = ""				for ch in html.split('/q?s=')[iter]:					if ch != "\"":						DJsym += ch					else:						break #Continue next iteration in outer 'for' loop when '"' is ran into.				DJlist.append(DJsym.encode('ascii'))			'''			pattern = re.compile('"(.+?)"')  #'.+' represents one-or-more-character string while '?' at the end represents non-greedy retrieval.			DJlist = pattern.findall(DJsym)  #Find all pattern in SPsym and return them as a list. Note: no need to predefine (SPlist=[]).			DJlist = sorted(DJlist)			print DJlist			#outfile.writerow(['Last Trading Date', 'Symbol', 'Last Price', '52-week Change', '52-week Low', '52-week High', '5 Year Average Dividend Yield', 'Trailing P/E', 'Forward P/E', 'PEG Ratio', 'Price/Sales', 'Price/Book', 'Market Cap', 'Levered Free Cash Flow', 'Market Per Cash Flow', 'Enterprise Value/EBITDA', 'Name'])			for tick in DJlist:				#print tick				response = requests.get('https://query2.finance.yahoo.com/v10/finance/quoteSummary/'+tick+'?formatted=true&crumb=Z3LBeFwaCFt&lang=en-US&region=US&modules=defaultKeyStatistics%2CfinancialData%2CsummaryDetail%2CcalendarEvents&corsDomain=finance.yahoo.com')				html = response.text  #Cnnvert requests object to string.				#if 'tabledata1\">' in html:				if html:					LP = self.StrFet('"currentPrice":{"raw":', 1, ",")					_52WkChg = self.StrFet('"52WeekChange":{"raw":', 1, ",")					_52WkHi = self.StrFet('"fiftyTwoWeekHigh":{"raw":', 1, ",")					_52WkLo = self.StrFet('"fiftyTwoWeekLow":{"raw":', 1, ",")					Div = self.StrFet('"trailingAnnualDividendYield":{"raw":', 1, ",")					tPE = self.StrFet('"trailingPE":{"raw":', 1, ",")					fPE = self.StrFet('"forwardPE":{"raw":', 1, ",")					PEG = self.StrFet('"pegRatio":{"raw":', 1, ",")					PpS = self.StrFet('"priceToSalesTrailing12Months":{"raw":', 1, ",")					PpB = self.StrFet('"priceToBook":{"raw":', 1, ",")					MktCap = self.StrFet('"marketCap":{"raw":', 1, ",")					FCF = self.StrFet('"operatingCashflow":{"raw":', 1, ",")					if type(MktCap) is not str and type(FCF) is not str and float(FCF) != 0:#if MktCap != "N/A" or FCF != "N/A" or FCF != "0":  #Calculate MpC only when MktCap and FCF are present and not zero.						#print MktCap, FCF						MpC = float(MktCap)/float(FCF)						MpC = str(MpC)					else:						MpC = "N/A"					EpE = self.StrFet('"enterpriseToEbitda":{"raw":', 1, ",")					response = requests.get('https://query1.finance.yahoo.com/v10/finance/quoteSummary/'+tick+'?formatted=true&crumb=8z9aPzzV3E6&lang=en-US&region=US&modules=price%2CsummaryDetail&corsDomain=finance.yahoo.com')					html = response.text  #Converts page request to string variable.					Name = self.StrFet('"longName":"', 1, "\"")										outfile.writerow([today, tick, LP, _52WkChg, _52WkHi, _52WkLo, Div, tPE, fPE, PEG, PpS, PpB, MktCap, FCF, MpC, EpE, Name])				else:					outfile.writerow([today, tick]+['N/A']*15)  #Output when url is incorrect.		fields = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'FiftyTwoWkHi', 'FiftyTwoWkLo', 'DivYild', 'TrailPE', 'ForwardPE', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA', 'Name']  #Must match individual column names in models.py for entry into database.		with open('DJ_list.csv', 'rb') as file:  # May need to use absolute path when on Pythonanywhere server (i.e. use '/home/cqcum6er/my-first-blog/DJ_list.csv' as file path.)			infile = csv.reader(file, delimiter=",", quotechar='"')  #Specify csv item boundary.			LastRowDate = ""  #Reserve a variable for the date from last row .			#print type(LastRowDate)			for row in reversed(list(infile)):  #Read csv file in reverse order or the most recent entry 1st (must convert csv reader object to list format 1st with list().)				if row[0] == LastRowDate or LastRowDate == "":  #Keep write to database while the date is still the same as last entry.					Post.objects.create(**dict(zip(fields, row)))  #zip() combines two lists into one list of pairs of items from both lists (fields and row). dict() converts the list of pairs into a dictionary. (**{'key': 'value'}) is the equivalent of function(key='value').					LastRowDate = row[0]  #Mark the current date for comparison to the next date from the next row.				else:					break		'''		with open('DJ_list.csv', 'rb') as file:  # Need to use absolute path when on Pythonanywhere server (i.e. use '/home/cqcum6er/my-first-blog/DJ_list.csv' as file path.)			infile = csv.reader(file, delimiter=",", quotechar='"')  #Specify csv item boundary.			for row in infile:				Post.objects.create(**dict(zip(fields, row)))		'''