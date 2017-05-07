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
class FeedbackForm(forms.Form):
	contact_name = forms.CharField(required=True)
	contact_email = forms.EmailField(required=True)
	content = forms.CharField(required=True, widget=forms.Textarea)  #Makes the "content" field a larger Textarea.