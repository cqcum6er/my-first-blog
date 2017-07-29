'''
forms.py is similar to models.py, with each attribute being a field input.
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
class ContactForm(forms.Form):
	name = forms.CharField(error_messages={'required': 'Please enter your name.'})  #Display error message if no user input is received.
	email = forms.EmailField(required=False)
	message = forms.CharField(error_messages={'required': 'Please enter a message.'}, widget=forms.Textarea)  #Makes the "content" field a larger Textarea.