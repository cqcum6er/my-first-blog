from django.db import models
from django.contrib import admin
#from django.core.urlresolvers import reverse
import datetime

class Post(models.Model):  #Defines our model ('models' is a python class; 'Post' is an object; 'models.Model' corresponds to a table in a database, a subclass of django.db.)
#author, title, text, created_date, & published_date all correspond to column in the 'Post' table.
    #author = models.ForeignKey('auth.User')
    #title = models.CharField(max_length=200)
    #text = models.TextField()
    #created_date = models.DateTimeField(default=timezone.now)
    #published_date = models.DateTimeField(blank=True, null=True)
	Day = models.DateField(blank=False, default=datetime.date.today().strftime('%Y-%m-%d'))
	Symbol = models.CharField(max_length=20, default='N/A')  #Add default value so the initiated table will have prepopulated value.
	LastPrice = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkChg = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkHi = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkLo = models.CharField(max_length=30, default='N/A')
	DivYild = models.CharField(max_length=30, default='N/A')
	TrailPE = models.CharField(max_length=30, default='N/A')
	ForwardPE = models.CharField(max_length=30, default='N/A')
	PEG_Ratio = models.CharField(max_length=30, default='N/A')
	PpS = models.CharField(max_length=30, default='N/A')
	PpB = models.CharField(max_length=30, default='N/A')
	Market_Cap = models.CharField(max_length=30, default='N/A')
	Free_Cash_Flow = models.CharField(max_length=30, default='N/A')
	Market_per_CashFlow = models.CharField(max_length=30, default='N/A')
	Enterprise_per_EBITDA = models.CharField(max_length=30, default='N/A')
	Name = models.CharField(max_length=50, default='N/A')
	#def publish(self):  #publish is a function/method that adds current time to 'published_date' field for each instance.
        #self.published_date = timezone.now()
        #self.save()

	#class Meta:  #To be used with .latest() in views.py.
		#get_latest_by = 'Day'

	def __str__(self):  #Note: The _str_ method returns a string of each model instance on the admin page; can be replaced with __unicode__(self).
		return self.Symbol
		#return self.title #Get a text (string) with a Post title
	'''
	def get_absolute_url(self):
		return reverse("blog:results", kwargs={"Symbol":self.Symbol})  #"<namespace>:<html>"
	'''

class SP500_Post(models.Model):
	Day = models.DateField(blank=False, default=datetime.date.today().strftime('%Y-%m-%d'))
	Symbol = models.CharField(max_length=20, default='N/A')
	LastPrice = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkChg = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkHi = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkLo = models.CharField(max_length=30, default='N/A')
	DivYild = models.CharField(max_length=30, default='N/A')
	TrailPE = models.CharField(max_length=30, default='N/A')
	ForwardPE = models.CharField(max_length=30, default='N/A')
	PEG_Ratio = models.CharField(max_length=30, default='N/A')
	PpS = models.CharField(max_length=30, default='N/A')
	PpB = models.CharField(max_length=30, default='N/A')
	Market_Cap = models.CharField(max_length=30, default='N/A')
	Free_Cash_Flow = models.CharField(max_length=30, default='N/A')
	Market_per_CashFlow = models.CharField(max_length=30, default='N/A')
	Enterprise_per_EBITDA = models.CharField(max_length=30, default='N/A')
	Name = models.CharField(max_length=50, default='N/A')

	def __str__(self):
		return self.Symbol

class NASDAQ_Post(models.Model):
	Day = models.DateField(blank=False, default=datetime.date.today().strftime('%Y-%m-%d'))
	Symbol = models.CharField(max_length=20, default='N/A')
	LastPrice = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkChg = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkHi = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkLo = models.CharField(max_length=30, default='N/A')
	DivYild = models.CharField(max_length=30, default='N/A')
	TrailPE = models.CharField(max_length=30, default='N/A')
	ForwardPE = models.CharField(max_length=30, default='N/A')
	PEG_Ratio = models.CharField(max_length=30, default='N/A')
	PpS = models.CharField(max_length=30, default='N/A')
	PpB = models.CharField(max_length=30, default='N/A')
	Market_Cap = models.CharField(max_length=30, default='N/A')
	Free_Cash_Flow = models.CharField(max_length=30, default='N/A')
	Market_per_CashFlow = models.CharField(max_length=30, default='N/A')
	Enterprise_per_EBITDA = models.CharField(max_length=30, default='N/A')
	Name = models.CharField(max_length=50, default='N/A')

	def __str__(self):
		return self.Symbol

class sp500_post_sorted(models.Model):
	Day = models.DateField(blank=False, default=datetime.date.today().strftime('%Y-%m-%d'))
	Symbol = models.CharField(max_length=20, default='N/A')
	LastPrice = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkChg = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkHi = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkLo = models.CharField(max_length=30, default='N/A')
	DivYild = models.CharField(max_length=30, default='N/A')
	TrailPE = models.CharField(max_length=30, default='N/A')
	ForwardPE = models.CharField(max_length=30, default='N/A')
	PEG_Ratio = models.CharField(max_length=30, default='N/A')
	PpS = models.CharField(max_length=30, default='N/A')
	PpB = models.CharField(max_length=30, default='N/A')
	Market_Cap = models.CharField(max_length=30, default='N/A')
	Free_Cash_Flow = models.CharField(max_length=30, default='N/A')
	Market_per_CashFlow = models.CharField(max_length=30, default='N/A')
	Enterprise_per_EBITDA = models.CharField(max_length=30, default='N/A')
	Name = models.CharField(max_length=50, default='N/A')

	def __str__(self):
		return self.Symbol

class all_ks(models.Model):
	Day = models.DateField(db_index=True, blank=False, default=datetime.date.today().strftime('%Y-%m-%d'))
	Symbol = models.CharField(db_index=True, max_length=20, default='N/A')
	#LastPrice_v0 = models.CharField(db_index=True, max_length=30, default='N/A')
	LastPrice = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=10)
	#FiftyTwoWkChg_v0 = models.CharField(db_index=True, max_length=30, default='N/A')
	FiftyTwoWkChg = models.DecimalField(blank=True, null=True, decimal_places=10, max_digits=15)
	FiftyTwoWkHi = models.CharField(db_index=True, max_length=30, default='N/A')
	FiftyTwoWkLo = models.CharField(db_index=True, max_length=30, default='N/A')
	#DivYild_v0 = models.CharField(db_index=True, max_length=30, default='N/A')
	DivYild = models.DecimalField(blank=True, null=True, decimal_places=10, max_digits=15)
	#TrailPE_v0 = models.CharField(db_index=True, max_length=30, default='N/A')
	TrailPE = models.DecimalField(blank=True, null=True, decimal_places=10, max_digits=20)
	ForwardPE = models.CharField(db_index=True, max_length=30, default='N/A')
	PEG_Ratio = models.CharField(db_index=True, max_length=30, default='N/A')
	PpS = models.CharField(db_index=True, max_length=30, default='N/A')
	PpB = models.CharField(db_index=True, max_length=30, default='N/A')
	Market_Cap = models.CharField(db_index=True, max_length=30, default='N/A')
	Free_Cash_Flow = models.CharField(db_index=True, max_length=30, default='N/A')
	Market_per_CashFlow = models.CharField(db_index=True, max_length=30, default='N/A')
	Enterprise_per_EBITDA = models.CharField(db_index=True, max_length=30, default='N/A')
	Name = models.CharField(db_index=True, max_length=50, default='N/A')
	'''
	SECTORS = (
		('BM', 'Basic Materials'),
		('CS', 'Communication Services'),
		('CC', 'Consumer Cyclical'),
		('CD', 'Consumer Defensive'),
		('E', 'Energy'),
		('FS', 'Financial Services'),
		('H', 'Healthcare'),
		('I', 'Industrials'),
		('RE', 'Real Estate'),
		('T', 'Technology'),
		('U', 'Utilities'),
	)
	'''
	Sector = models.CharField(db_index=True, max_length=50, default='N/A')  #choices=SECTORS

	def __str__(self):
		return self.Symbol

class all_ks_DatePriceDiff(models.Model):
	Day = models.DateField(blank=False, default=datetime.date.today().strftime('%Y-%m-%d'))
	Name = models.CharField(max_length=50, default='N/A')
	Symbol = models.CharField(max_length=20, default='N/A')
	Price_1 = models.DecimalField(blank=True, null=True, decimal_places=3, max_digits=10)
	Price_7 = models.DecimalField(blank=True, null=True, decimal_places=3, max_digits=10)
	Price_30 = models.DecimalField(blank=True, null=True, decimal_places=3, max_digits=10)

	def __str__(self):
		return self.Symbol

class all_ks_join(models.Model):
	Day = models.DateField(blank=False, default=datetime.date.today().strftime('%Y-%m-%d'))
	Symbol = models.CharField(max_length=20, default='N/A')
	LastPrice = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkChg = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkHi = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkLo = models.CharField(max_length=30, default='N/A')
	DivYild = models.CharField(max_length=30, default='N/A')
	TrailPE = models.CharField(max_length=30, default='N/A')
	ForwardPE = models.CharField(max_length=30, default='N/A')
	PEG_Ratio = models.CharField(max_length=30, default='N/A')
	PpS = models.CharField(max_length=30, default='N/A')
	PpB = models.CharField(max_length=30, default='N/A')
	Market_Cap = models.CharField(max_length=30, default='N/A')
	Free_Cash_Flow = models.CharField(max_length=30, default='N/A')
	Market_per_CashFlow = models.CharField(max_length=30, default='N/A')
	Enterprise_per_EBITDA = models.CharField(max_length=30, default='N/A')
	Name = models.CharField(max_length=50, default='N/A')

	def __str__(self):
		return self.Symbol

class all_ks_join_unique(models.Model):
	Day = models.DateField(blank=False, default=datetime.date.today().strftime('%Y-%m-%d'))
	Symbol = models.CharField(max_length=20, default='N/A')
	LastPrice = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkChg = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkHi = models.CharField(max_length=30, default='N/A')
	FiftyTwoWkLo = models.CharField(max_length=30, default='N/A')
	DivYild = models.CharField(max_length=30, default='N/A')
	TrailPE = models.CharField(max_length=30, default='N/A')
	ForwardPE = models.CharField(max_length=30, default='N/A')
	PEG_Ratio = models.CharField(max_length=30, default='N/A')
	PpS = models.CharField(max_length=30, default='N/A')
	PpB = models.CharField(max_length=30, default='N/A')
	Market_Cap = models.CharField(max_length=30, default='N/A')
	Free_Cash_Flow = models.CharField(max_length=30, default='N/A')
	Market_per_CashFlow = models.CharField(max_length=30, default='N/A')
	Enterprise_per_EBITDA = models.CharField(max_length=30, default='N/A')
	Name = models.CharField(max_length=50, default='N/A')

	def __str__(self):
		return self.Symbol

class Index_DJ(models.Model):
	Day = models.DateField(blank=False, default=datetime.date.today().strftime('%Y-%m-%d'))
	Symbol = models.CharField(max_length=20, default='N/A')

	def __str__(self):
		return self.Symbol

class Index_SP500(models.Model):
	Day = models.DateField(blank=False, default=datetime.date.today().strftime('%Y-%m-%d'))
	Symbol = models.CharField(max_length=20, default='N/A')

	def __str__(self):
		return self.Symbol

class UserComment(models.Model):  #A model object for user input data on form object, ContactForm (see 'forms.py').
	name = models.CharField(max_length=80)
	email = models.EmailField()
	message = models.TextField(max_length=2000)  #Use "TextField" to avoid limits imposed to string length by Django or SQL.
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name