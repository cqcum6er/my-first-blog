#Test whether csv entry is entered correctly into database thru python command prompt:>python test.py
import csv
'''
def handle(self, *args, **options):
	global html  #Makes html accessible to all functions (StrFet and handle).
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