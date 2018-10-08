'''
forms.py is similar to models.py, with each attribute being a field input; use forms.py to further customize form appearance (use ModelForm if a form is linked to a model object).
'''
from django import forms

'''
from .models import Post
#Use the following model form if each feedback form is linked to each model instance.
class FeedbackForm(forms.ModelForm):
	class Meta:
		model = Post
		#fields = ['title', 'text',]
		exclude = []
'''
#Use the following form if feedback isn't linked to model instances.
class ContactForm(forms.Form):  #Modify what the user sees.
	name = forms.CharField(error_messages={'required': 'Please enter your name.'})  #Display custom error message if no user input is received.
	email = forms.EmailField(required=False)
	message = forms.CharField(error_messages={'required': 'Please enter a message.'}, widget=forms.Textarea)  #Use widget to makes the "content" field a larger Textarea.

class IndexForm(forms.Form):
	Ind_Date = forms.ChoiceField(choices=[('1', 'Trading Day'), ('7', 'Week'), ('91', 'Quarter'), ('183', '6 months'), ('365', 'Year')])

class MoverForm(forms.Form):
	Ind_Mov = forms.ChoiceField(choices=[('Index_DJ', 'Dow Jones'), ('Index_SP500', 'S&P500')])  #Get Ind_Mov value from template with {{form.Ind_Mov}}; choices=[(value, label)]
	Period_Mov = forms.ChoiceField(choices=[('1', 'One Day'), ('7', 'One Week'), ('30', 'One Month')])
	Dis_num = forms.ChoiceField(choices=[('5', '5'), ('10', '10')])
