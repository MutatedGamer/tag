from django import forms
from main.models import CustomGroup

class CustomGroupForm(forms.ModelForm):
	class Meta:
		model = CustomGroup
		fields = ('name', 'moderated',  'photo') 
