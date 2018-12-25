#To run, go to folder containing manage.py with the following command: >python manage.py [script name]#To update local database, 'index_DJ.py' and 'index_SP500.py' must be ran 1st, followed by 'index_combo.py' and then 'index_combo2.py'#Combine 'index_DJ.csv' & 'index_SP500.csv' into one file ('index_LastCombo.csv') of ticker symbols from the latest entry and convert the file content into a set ('index_LastComboSet.csv').  Avoid rejection from server, scrape from Yahoo Finance the key statistics of the symbol set from A to H and write them to a file ('index_LastComboSet_ks.csv').from django.core.management.base import BaseCommand, CommandError  #For Pythonanywhere schedule tasks.#from django.http import StreamingHttpResponse  #Use to avoid a load balancer dropping a connection while the server was generating the response.import stringimport csvimport requestsimport randomimport datetimeimport time#from blog.models import all_ksclass Command(BaseCommand):	help = "Combine ticker symbols from DJ and S&P500 indices"	def StrFet(self, sep, num, end):  #StrFet() function fetches components of key statistics page; att=attribute, sep=separator, num=Nth separator, end=delimiter.		if sep not in html:  #Return "N/A" when no substring is found.			return "N/A"		else:			att = ""			for ch in html.split(sep)[num]:				if ch != end:					att += ch				else:					break #terminates the nearest enclosing loop when '<' is ran into (the loop control target, ch, keeps its current value).			if att[0] == '"':  #Return "N/A" if raw is contained in '"' (something other than a number).				return "N/A"			else:				return att	def handle(self, *args, **options):  #For use with Command(BaseCommand).		global html  #Makes html accessible to all functions (StrFet and handle).				filenames = ['index_DJ.csv', 'index_SP500.csv']  #List all files to append to outfile.		with open('index_LastCombo.csv', 'wb') as outfile:  #Combine all indices from the most recent date, overwriting previous version instead of appending.			outfile = csv.writer(outfile, delimiter=",", quotechar='"')			#print type(outfile)			for fname in filenames:  #Iterate thru DJ and SP500 index csv.				with open(fname) as infile:  #Read the content of each fname as infile.					infile = csv.reader(infile, delimiter=",", quotechar='"')					LastRowDate = ""  #Reserve a variable for the date from last row.					for row in reversed(list(infile)):  #Read from last day of each index.						if row[0] == LastRowDate or LastRowDate == "":  #Keep writing to database until the date changes.							#print row							outfile.writerow(row)							LastRowDate = row[0]  #Update the current date for comparison to the next date in the next row.						else:							break		content = open('index_LastCombo.csv', 'rb').readlines()  #Read lines from file and collect the lines in a list; .readlines() isn't compatible with 'with...as...'.		content_set = sorted(set(content))  #Trim combined index into a set of non-redundant symbols.		#print content_set		cleandata = open('index_LastComboSet.csv', 'wb')  #Prepare a new output file to write out the set.		for line in content_set:			cleandata.write(line)		cleandata.close()  #Need to close writer for 'index_LastComboSet.csv' before it can be read properly again next time.		with open('index_LastComboSet_ks.csv', 'wb') as ks_file:  #Use 'wb' (write to binary) to avoid writing out extra line on Windows machine.			output = csv.writer(ks_file, delimiter=",", quotechar='"')			#output.writerow('test')			with open('index_LastComboSet.csv', 'rb') as file:				infile = csv.reader(file, delimiter=",", quotechar='"')				#LastRowDate = ""				#print list(string.ascii_uppercase)[:8]				for row in list(infile):					#if row[1]:  #Check if ticker for each row is empty.					#if row[1][1] in ["A", "B"]:  #Check if the 1st char in ticker symbol matches defined char.					#tick = row[1]  #.encode('utf-8')					#row[0] = date, row[1] = ticker					#print row					if row[1][0] in list(string.ascii_uppercase)[:8]:  #Check if the 1st char of ticker symbol (row[1]) matches any alphabet from A to H.						#if row[0] == LastRowDate or LastRowDate == "":						time.sleep(random.randint(0,2))						#print row, len(row)						response = requests.get('https://query2.finance.yahoo.com/v10/finance/quoteSummary/'+row[1]+'?formatted=true&crumb=Z3LBeFwaCFt&lang=en-US&region=US&modules=defaultKeyStatistics%2CfinancialData%2CsummaryDetail%2CcalendarEvents&corsDomain=finance.yahoo.com')						html = response.text  #Convert requests object to string.						#print html						if html:							#print 'html present'							LP = self.StrFet('"currentPrice":{"raw":', 1, ",")							_52WkChg = self.StrFet('"52WeekChange":{"raw":', 1, ",")							_52WkHi = self.StrFet('"fiftyTwoWeekHigh":{"raw":', 1, ",")							_52WkLo = self.StrFet('"fiftyTwoWeekLow":{"raw":', 1, ",")							Div = self.StrFet('"trailingAnnualDividendYield":{"raw":', 1, ",")							tPE = self.StrFet('"trailingPE":{"raw":', 1, ",")							fPE = self.StrFet('"forwardPE":{"raw":', 1, ",")							PEG = self.StrFet('"pegRatio":{"raw":', 1, ",")							PpS = self.StrFet('"priceToSalesTrailing12Months":{"raw":', 1, ",")							PpB = self.StrFet('"priceToBook":{"raw":', 1, ",")							MktCap = self.StrFet('"marketCap":{"raw":', 1, ",")							FCF = self.StrFet('"operatingCashflow":{"raw":', 1, ",")							if type(MktCap) is not str and type(FCF) is not str and float(FCF) != 0:#if MktCap != "N/A" or FCF != "N/A" or FCF != "0":  #Calculate MpC only when MktCap and FCF are present and not zero.								#print MktCap, FCF								MpC = float(MktCap)/float(FCF)								MpC = str(MpC)							else:								MpC = "N/A"							EpE = self.StrFet('"enterpriseToEbitda":{"raw":', 1, ",")							response = requests.get('https://query1.finance.yahoo.com/v10/finance/quoteSummary/'+row[1]+'?formatted=true&crumb=8z9aPzzV3E6&lang=en-US&region=US&modules=price%2CsummaryDetail&corsDomain=finance.yahoo.com')							html = response.text  #Converts page request to string variable.							if html:								if '"longName":' in html:  #Escape when "longName" isn't present.									longNameToEnd = ""									for ch in html.split('"longName":')[1]:  #Retrieve all character containing longName plus everything after.										longNameToEnd += ch									longNameSplit = longNameToEnd.split(',\"')  #Terminate character retrieval before the next field variable.									#print longNameSplit[0], longNameSplit[0].count('"')									if longNameSplit[0].count('"') >= 2:  #If longName is contained within '"' mark...										longNameInQuote = longNameSplit[0].replace('amp;','').replace('&apos;',"'")  #Replace html escape character for "&" and "'".										Name = longNameInQuote.encode('utf-8')  #... convert to byte string from unicode.										#Name = Name[1:-1]  #Remove quotation marks from ends.										#if Name[0] != '"':  #Inser '"' to the beginning and end of Name if not already present.											#Name = '"' + Name + '"'									else:  #...return "N/A" if longName is null.										Name = "N/A"								else:									Name = "N/A"							else:  #Return "N/A" if Name isn't retrievable from assigned html.								Name = "N/A"							response = requests.get('https://query1.finance.yahoo.com/v10/finance/quoteSummary/'+row[1]+'?formatted=true&crumb=fHNmbuf4JOf&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents%2CesgScores%2Cdetails&corsDomain=finance.yahoo.com')							html = response.text  #Convert requests object to string.							#print html							if html:								Sector = self.StrFet('"sector":', 1, ",")							else:								Sector = "N/A"							#print row[0], row[1], LP, _52WkChg, _52WkHi, _52WkLo, Div, tPE, fPE, PEG, PpS, PpB, MktCap, FCF, MpC, EpE, Name							csv_row_list = [row[0], row[1], LP, _52WkChg, _52WkHi, _52WkLo, Div, tPE, fPE, PEG, PpS, PpB, MktCap, FCF, MpC, EpE, Name, Sector]							#StreamingHttpResponse(output.writerow(csv_row_list))							output.writerow(csv_row_list)						else:							output.writerow([row[0], row[1]]+['N/A']*16)  #Output when url is incorrect.							#StreamingHttpResponse(output.writerow([row[0], row[1]]+['N/A']*15))							#LastRowDate = row[0]						#else:  #Skip a ticker if date is not the same as previous row to account for incomplete date.							#continue							#output.writerow(['N/A']*17)  #Output when csv row is empty.					else:  #Retrieve the remaining [I-Z] ticker key statistics in "iindex_combo2.py"						break