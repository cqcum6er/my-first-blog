#To run, go to folder containing manage.py with the following command: >python manage.py [script name]
from django.core.management.base import BaseCommand, CommandError
from django.http import StreamingHttpResponse  #Use to avoid a load balancer dropping a connection while the server was generating the response.
import string
import csv
import requests
import random
import datetime
import time
from blog.models import all_ks

class Command(BaseCommand):
	help = "Combine ticker symbols from DJ and S&P500 indices"

	def StrFet(self, sep, num, end):  #StrFet() function fetches components of key statistics page; att=attribute, sep=separator, num=Nth separator, end=delimiter.
		if sep not in html:  #Return "N/A" when no substring is found.
			return "N/A"
		else:
			att = ""
			for ch in html.split(sep)[num]:
				if ch != end:
					att += ch
				else:
					break #terminates the nearest enclosing loop when '<' is ran into (the loop control target, ch, keeps its current value).
			if att[0] == '"':  #Return "N/A" if raw is contained in '"' (something other than a number).
				return "N/A"
			else:
				return att

	def handle(self, *args, **options):
		global html  #Makes html accessible to all functions (StrFet and handle).
		'''
		filenames = ['index_DJ.csv', 'index_SP500.csv']  #List all files to append to outfile.
		with open('index_LastCombo.csv', 'wb') as outfile:  #Combine all indices from the most recent date.
			outfile = csv.writer(outfile, delimiter=",", quotechar='"')
			#print type(outfile)
			for fname in filenames:
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

		content = open('index_LastCombo.csv', 'rb').readlines()  #Read lines from file and collect the lines in a list; cannot use with...as... format due to .readlines().
		content_set = sorted(set(content))  #Condense all indices into a set.
		print content_set
		cleandata = open('index_LastComboSet.csv', 'wb')  #Prepare a new output file to write out the set.
		for line in content_set:
			cleandata.write(line)

		with open('index_LastComboSet_ks.csv', 'wb') as ks_file:  #Use 'wb' (write to binary) to avoid writing out extra line on Windows machine.
			output = csv.writer(ks_file, delimiter=",", quotechar='"')
			#output.writerow('test')
			with open('index_LastComboSet.csv', 'rb') as file:
				infile = csv.reader(file, delimiter=",", quotechar='"')
				LastRowDate = ""
				print list(string.ascii_uppercase)[:8]
				for row in list(infile):
					#if row[1]:  #Check if ticker for each row is empty.
					#if row[1][1] in ["A", "B"]:  #Check if the 1st char in ticker symbol matches defined char.
					#tick = row[1]  #.encode('utf-8')
					#row[0] = date, row[1] = ticker.
					if row[1][0] in list(string.ascii_uppercase)[:8]:  #Check if the 1st char of ticker symbol matches any alphabet from A to H.
						if row[0] == LastRowDate or LastRowDate == "":
							#time.sleep(random.randint(0,2))
							print row, len(row)
							response = requests.get('https://query2.finance.yahoo.com/v10/finance/quoteSummary/'+row[1]+'?formatted=true&crumb=Z3LBeFwaCFt&lang=en-US&region=US&modules=defaultKeyStatistics%2CfinancialData%2CsummaryDetail%2CcalendarEvents&corsDomain=finance.yahoo.com')
							html = response.text  #Convert requests object to string.
							#print html
							if html:
								#print 'html present'
								LP = self.StrFet('"currentPrice":{"raw":', 1, ",")
								_52WkChg = self.StrFet('"52WeekChange":{"raw":', 1, ",")
								_52WkHi = self.StrFet('"fiftyTwoWeekHigh":{"raw":', 1, ",")
								_52WkLo = self.StrFet('"fiftyTwoWeekLow":{"raw":', 1, ",")
								Div = self.StrFet('"trailingAnnualDividendYield":{"raw":', 1, ",")
								tPE = self.StrFet('"trailingPE":{"raw":', 1, ",")
								fPE = self.StrFet('"forwardPE":{"raw":', 1, ",")
								PEG = self.StrFet('"pegRatio":{"raw":', 1, ",")
								PpS = self.StrFet('"priceToSalesTrailing12Months":{"raw":', 1, ",")
								PpB = self.StrFet('"priceToBook":{"raw":', 1, ",")
								MktCap = self.StrFet('"marketCap":{"raw":', 1, ",")
								FCF = self.StrFet('"operatingCashflow":{"raw":', 1, ",")
								if type(MktCap) is not str and type(FCF) is not str and float(FCF) != 0:#if MktCap != "N/A" or FCF != "N/A" or FCF != "0":  #Calculate MpC only when MktCap and FCF are present and not zero.
									#print MktCap, FCF
									MpC = float(MktCap)/float(FCF)
									MpC = str(MpC)
								else:
									MpC = "N/A"
								EpE = self.StrFet('"enterpriseToEbitda":{"raw":', 1, ",")
								response = requests.get('https://query1.finance.yahoo.com/v10/finance/quoteSummary/'+row[1]+'?formatted=true&crumb=8z9aPzzV3E6&lang=en-US&region=US&modules=price%2CsummaryDetail&corsDomain=finance.yahoo.com')
								html = response.text  #Converts page request to string variable.
								if html:
									longNameToEnd = ""
									for ch in html.split('"longName":')[1]:  #Retrieve all character containing longName plus everything after.
										longNameToEnd += ch
									longNameSplit = longNameToEnd.split(',\"')  #Terminate character retrieval before the next field variable.
									#print longNameSplit[0], longNameSplit[0].count('"')
									if longNameSplit[0].count('"') >= 2:  #If longName is contained within '"' mark...
										longNameInQuote = longNameSplit[0].replace('amp;','').replace('&apos;',"'")  #Replace html escape character for "&" and "'".
										Name = longNameInQuote.encode('utf-8')  #... convert to byte string from unicode.
										#Name = Name[1:-1]  #Remove quotation marks from ends.
										#if Name[0] != '"':  #Inser '"' to the beginning and end of Name if not already present.
											#Name = '"' + Name + '"'
									else:  #...return "N/A" if longName is null.
										Name = "N/A"
								else:  #Return "N/A" if Name isn't retrievable from assigned html.
									Name = "N/A"
								print row[0], row[1], LP, _52WkChg, _52WkHi, _52WkLo, Div, tPE, fPE, PEG, PpS, PpB, MktCap, FCF, MpC, EpE, Name
								csv_row_list = [row[0], row[1], LP, _52WkChg, _52WkHi, _52WkLo, Div, tPE, fPE, PEG, PpS, PpB, MktCap, FCF, MpC, EpE, Name]
								output.writerow(csv_row_list)
							else:
								output.writerow([row[0], row[1]]+['N/A']*15)  #Output when url is incorrect.
							LastRowDate = row[0]
						else:  #Skip a ticker if date is not the same as previous row to account for incomplete date.
							continue
							#output.writerow(['N/A']*17)  #Output when csv row is empty.
					else:
						break
		'''
		with open('index_LastComboSet_ks.csv', 'ab') as ks_file:  #Use 'ab' (append to binary) to add the remaining ticker key stats.
			output = csv.writer(ks_file, delimiter=",", quotechar='"')
			with open('index_LastComboSet.csv', 'rb') as file:
				infile = csv.reader(file, delimiter=",", quotechar='"')
				#LastRowDate = ""
				print list(string.ascii_uppercase)[8:]
				for row in list(infile):
					if row[1]:
						if row[1][0] in list(string.ascii_uppercase)[8:]:  #Check if the 1st char of ticker symbol matches any alphabet from I to Z.
						#if row[0] == LastRowDate or LastRowDate == "":
							print row, len(row)
							time.sleep(random.randint(0,2))
							response = requests.get('https://query2.finance.yahoo.com/v10/finance/quoteSummary/'+row[1]+'?formatted=true&crumb=Z3LBeFwaCFt&lang=en-US&region=US&modules=defaultKeyStatistics%2CfinancialData%2CsummaryDetail%2CcalendarEvents&corsDomain=finance.yahoo.com')
							html = response.text  #Convert requests object to string.
							#response = requests.get('https://finance.yahoo.com/quote/'+row[1]+'/key-statistics?p='+row[1])
							#html = response.json()
							#print html
							if html:
								#print 'html present'
								LP = self.StrFet('"currentPrice":{"raw":', 1, ",")
								_52WkChg = self.StrFet('"52WeekChange":{"raw":', 1, ",")
								_52WkHi = self.StrFet('"fiftyTwoWeekHigh":{"raw":', 1, ",")
								_52WkLo = self.StrFet('"fiftyTwoWeekLow":{"raw":', 1, ",")
								Div = self.StrFet('"trailingAnnualDividendYield":{"raw":', 1, ",")
								tPE = self.StrFet('"trailingPE":{"raw":', 1, ",")
								fPE = self.StrFet('"forwardPE":{"raw":', 1, ",")
								PEG = self.StrFet('"pegRatio":{"raw":', 1, ",")
								PpS = self.StrFet('"priceToSalesTrailing12Months":{"raw":', 1, ",")
								PpB = self.StrFet('"priceToBook":{"raw":', 1, ",")
								MktCap = self.StrFet('"marketCap":{"raw":', 1, ",")
								FCF = self.StrFet('"operatingCashflow":{"raw":', 1, ",")
								if type(MktCap) is not str and type(FCF) is not str and float(FCF) != 0:#if MktCap != "N/A" or FCF != "N/A" or FCF != "0":  #Calculate MpC only when MktCap and FCF are present and not zero.
									#print MktCap, FCF
									MpC = float(MktCap)/float(FCF)
									MpC = str(MpC)
								else:
									MpC = "N/A"
								EpE = self.StrFet('"enterpriseToEbitda":{"raw":', 1, ",")
								response = requests.get('https://query1.finance.yahoo.com/v10/finance/quoteSummary/'+row[1]+'?formatted=true&crumb=8z9aPzzV3E6&lang=en-US&region=US&modules=price%2CsummaryDetail&corsDomain=finance.yahoo.com')
								html = response.text  #Converts page request to string variable.
								if html:
									if '"longName":' in html:  #Escape when "longName" isn't present.
										longNameToEnd = ""
										for ch in html.split('"longName":')[1]:  #Retrieve all character containing longName plus everything after.
											longNameToEnd += ch
										longNameSplit = longNameToEnd.split(',\"')  #Terminate character retrieval before the next field variable.
										#print longNameSplit[0], longNameSplit[0].count('"')
										if longNameSplit[0].count('"') >= 2:  #If longName is contained within '"' mark...
											longNameInQuote = longNameSplit[0].replace('amp;','').replace('&apos;',"'")  #Replace html escape character for "&" and "'".
											Name = longNameInQuote.encode('utf-8')  #... convert to byte string from unicode.
										else:  #...return "N/A" if longName is null.
											Name = "N/A"
									else:
										Name = "N/A"
								else:  #Return "N/A" if Name isn't retrievable from assigned html.
									Name = "N/A"
								#print row[0], row[1], LP, _52WkChg, _52WkHi, _52WkLo, Div, tPE, fPE, PEG, PpS, PpB, MktCap, FCF, MpC, EpE, Name
								csv_row_list = [row[0], row[1], LP, _52WkChg, _52WkHi, _52WkLo, Div, tPE, fPE, PEG, PpS, PpB, MktCap, FCF, MpC, EpE, Name]
								StreamingHttpResponse(output.writerow(csv_row_list))
							else:
								StreamingHttpResponse(output.writerow([row[0], row[1]]+['N/A']*15))  #Output when url is incorrect.
							#LastRowDate = row[0]
						else:  #Skip a ticker if tick is not retrivable.
							continue
					else:  #...continue iterate until the end.
						continue

		fields = ['Day', 'Symbol', 'LastPrice', 'FiftyTwoWkChg', 'FiftyTwoWkLo', 'FiftyTwoWkHi', 'DivYild', 'TrailPE', 'ForwardPE', 'PEG_Ratio', 'PpS', 'PpB', 'Market_Cap', 'Free_Cash_Flow', 'Market_per_CashFlow', 'Enterprise_per_EBITDA', 'Name']  #Must match individual field (column) names in models.py.
		if all_ks.objects.exists():  #Check if the database is empty...
			#print "There are existing objects in all_ks db."
			p = all_ks.objects.latest('Day')  #Check what's the lastest day then append to db from then on.
			with open('index_LastComboSet_ks.csv', 'rb') as file:  # Need to use absolute path when on Pythonanywhere server (i.e. use '/home/cqcum6er/my-first-blog/DJ_list.csv' as file path.)
				infile = csv.reader(file, delimiter=",", quotechar='"')  #Specify csv item boundary.
				for row in infile:
					row_datetime = datetime.datetime.strptime(row[0],'%Y-%m-%d')  #row[0] is converted from str to datetime format.
					#print row_datetime.date(), type(row_datetime.date())
					row_date = row_datetime.date()  #Converting from datetime to date.
					#print type(row_date), "converted to 'date' format", p.Day
					if row_date > p.Day:  #Only append entry if the date of the entry is later than the most recent in db.
						#print row_date
						all_ks.objects.create(**dict(zip(fields, row)))
		else:  #...append all rows if the database is empty.
			with open('index_LastComboSet_ks.csv', 'rb') as file:
				infile = csv.reader(file, delimiter=",", quotechar='"')
				for row in infile:
					all_ks.objects.create(**dict(zip(fields, row)))