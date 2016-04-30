from django.core.management.base import BaseCommand, CommandError
import csv
import requests
from blog.models import Post

def populate():
	with open(TICKERS, 'rU') as csvfile:
		file = csv.reader(csvfile, delimiter=',')
		for row in file:
			add_ticker(str(row[0]), str(row[1]))

def add_ticker(name, ticker):
	c = Symbol.objects.get_or_create(name=name, ticker=ticker)
	return c
