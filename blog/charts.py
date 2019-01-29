import pygal
from .models import all_ks

class FundGraph():
	def __init__(self, **kwargs):
		self.chart = pygal.Line(**kwargs)
		self.chart.title = 'Price History'

	def get_data(self):
		#Query the db for chart data, pack them into a dict and return it.
		data = {}
		for daily in all_ks.objects.filter(Symbol__iexact='AAPL'): #.order_by('Day'):
			data[daily.Day] = daily.LastPrice
		return data

	def generate(self):
		# Get chart data
		chart_data = self.get_data()

		# Add data to chart
		for key, value in chart_data.items():
			self.chart.add(key, value)

		# Return the rendered SVG
		return self.chart.render_data_uri(is_unicode=True)
		#return self.chart.render_data_uri()
		#return self.chart.render_data_uri(is_unicode=True)
	