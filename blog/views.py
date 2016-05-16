from django.shortcuts import render
from .models import Post  #'Post' table object is retrieved from 'models.py' within the same folder.
import requests
import csv

def post_list(request):  #Home url
	return render(request, 'blog/home.html')

def inProgrss(request):  #In-Progress url
	return render(request, 'blog/InProgress.html')

def KeyFet(sep,num):  #KeyFet() function fetches components of key statistics page; att=attribute, sep=separator, num=Nth separator
	att = ""
	for ch in html.split(sep)[num]:
		if ch != "<":
			att += ch
		else:
			break #terminates the nearest enclosing loop when '<' is ran into (the loop control target, ch, keeps its current value).
	return att

def DJ_list(request):  #"post_list" must be requested from urls.py
	if Post:  #Check to see if there is existing entry.  If there is, delete existing entry to prepare for updated entry.
		Post.objects.all().delete()
	else:
		pass
	with open('./DJ_list.csv', 'rb') as file:
		infile = csv.reader(file, delimiter=",", quotechar='"')
		next(infile, None)  # skip the headers
		for row in infile:
			#if row.line_num == 1:
				#continue  #Skip column header.
			#post, created = Post.objects.get_or_create(
			post = Post(
			Symbol=row[0],
			LastPrice=row[1],
			FiftyTwoWkChg=row[2],
			FiftyTwoWkLo=row[3],
			FiftyTwoWkHi=row[4],
			DivYild=row[5],
			TrailPE=row[6],
			ForwardPE=row[7],
			PEG_Ratio=row[8],
			PpS=row[9],
			PpB=row[10],
			Market_Cap=row[11],
			Free_Cash_Flow=row[12],
			Market_per_CashFlow=row[13],
			Enterprise_per_EBITDA=row[14],
			Name=row[15],
			)
			post.save()  #Save each entry ('post') of database.
		posts = Post.objects.values()  #values() returns content of database as dictionary, thus making the database iterable.
		return render(request, 'blog/DJ.html', {'posts': posts})  #To serve as a template, 'blog/post_list.html' has to be put in blog\template\blog\
		#The last parameter, which looks like this: {} is a place to integrate objects in models.py (posts) with html ('posts') in template folder.
	'''
	#posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
	global html  #Make 'html' accessible to KeyFet function.
	response = requests.get('http://finance.yahoo.com/q/cp?s=%5EDJI+Components')
	html = response.text  #Convert requests object to string.
	DJlist = []
	for iter in xrange(5,35):
		DJsym = ""
		for ch in html.split('/q?s=')[iter]:
			if ch != "\"":
				DJsym += ch
			else:
				break #Continue next iteration in outer 'for' loop when '"' is ran into.
		DJlist.append(DJsym.encode('ascii'))
	#for tick in DJlist:
		#YFconn.request('GET','/q/ks?s='+tick+'+Key+Statistics')
	if Post:  #Check to see if there is existing entry.  If there is, delete existing entry to prepare for updated entry.
		Post.objects.all().delete()
	else:
		pass
	for tick in DJlist:
		#YFconn.request('GET','/q/ks?s='+tick+'+Key+Statistics')
		response = requests.get('http://finance.yahoo.com/q/ks?s='+tick+'+Key+Statistics')
		html = response.text  #Convert requests object to string.
		if 'tabledata1\">' in html:
			LastPrice = ""
			if 'yfs_l84_' in html:
				for ch in html.split('yfs_l84_')[1]:
					if ch != '<':
						LastPrice += ch
					else:
						break
				LP_Split = LastPrice.split('>')
				LP = LP_Split[1].replace(',','')
				print LP
			_52WkChg = ""
			for ch in html.split('tabledata1\">')[33]:
				if ch != "<":
					_52WkChg += ch
				else:
					break
			_52WkLo = KeyFet('tabledata1\">',36)
			_52WkHi = KeyFet('tabledata1\">',35)
			Div = KeyFet('tabledata1\">',53)
			tPE = KeyFet('tabledata1\">',3)
			fPE = KeyFet('tabledata1\">',4)
			PEG = KeyFet('tabledata1\">',5)
			PpS = KeyFet('tabledata1\">',6)
			PpB = KeyFet('tabledata1\">',7)
			MktCap = ""
			if 'yfs_j10_' in html:
				for ch in html.split('yfs_j10_')[1]:
					if ch != '<':
						MktCap += ch
					else:
						break
				MC_Split = MktCap.split('>')
				MktCap = MC_Split[1]
			else:
				MktCap = KeyFet('tabledata1\">',1)
			FCF = KeyFet('tabledata1\">',31)
			if MktCap[-1] == "T":
				MCflo = float(MktCap[:-1])*10**6
			elif MktCap[-1] == "B":
				MCflo = float(MktCap[:-1])*1000
			elif MktCap[-1] == "M":
				MCflo = float(MktCap[:-1])
			elif MktCap[-1] == "K":
				MCflo = float(MktCap[:-1])/1000
			else:
				continue
			if FCF[-1] == "B":
				FCFflo = float(FCF[:-1])*1000
				MpC = str(MCflo/FCFflo)
			elif FCF[-1] == "M":
				FCFflo = float(FCF[:-1])
				MpC = str(MCflo/FCFflo)
			elif FCF[-1] == "K":
				FCFflo = float(FCF[:-1])/1000
				MpC = str(MCflo/FCFflo)
			else:
				MpC = "N/A"
			EpE = KeyFet('tabledata1\">',9)
			Name = ""
			for ch in html.split('<h2>')[2]:
				if ch != "<":
					Name += ch
				else:
					break
		post = Post(
			Symbol=tick,
			LastPrice=LP,
			FiftyTwoWkChg=_52WkChg,
			FiftyTwoWkLo=_52WkLo,
			FiftyTwoWkHi=_52WkHi,
			DivYild=Div,
			TrailPE=tPE,
			ForwardPE=fPE,
			PEG_Ratio=PEG,
			PpS=PpS,
			PpB=PpB,
			Market_Cap=MktCap,
			Free_Cash_Flow=FCF,
			Market_per_CashFlow=MpC,
			Enterprise_per_EBITDA=EpE,
			Name=Name,
			)
		post.save()  #Save each entry of database.
	posts = Post.objects.values()  #values() returns content of database as dictionary, thus making the database iterable.
	return render(request, 'blog/DJ.html', {'posts': posts})  #To serve as a template, 'blog/post_list.html' has to be put in blog\template\blog\
	#The last parameter, which looks like this: {} is a place to integrate objects in models.py (posts) with html ('posts') in template folder.
	'''