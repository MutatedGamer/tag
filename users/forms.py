from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from PIL import Image
from django.core.files import File
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class CustomUserCreationForm(UserCreationForm):

	class Meta(UserCreationForm.Meta):
		model = CustomUser
		fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

	class Meta:
		model = CustomUser
		fields = '__all__' 

class CustomUserEditProfileForm(forms.ModelForm):
	x = forms.FloatField(widget=forms.HiddenInput())
	y = forms.FloatField(widget=forms.HiddenInput())
	width = forms.FloatField(widget=forms.HiddenInput())
	height = forms.FloatField(widget=forms.HiddenInput())

	class Meta:
		model = CustomUser
		fields =('bio', 'school', 'avatar', 'x', 'y', 'width', 'height',)

	def __init__(self, *args, **kwargs):
		super(CustomUserEditProfileForm, self).__init__(*args, **kwargs)
		self.fields['avatar'].required = False
		self.fields['x'].required = False
		self.fields['y'].required = False
		self.fields['width'].required = False
		self.fields['height'].required = False

	def save(self, **kwargs):
		to_change = super(CustomUserEditProfileForm, self).save(commit = False)


		if self.cleaned_data.get('x'):
			x = self.cleaned_data.get('x')
			y = self.cleaned_data.get('y')
			w = self.cleaned_data.get('width')
			h = self.cleaned_data.get('height')

			image = Image.open(to_change.avatar)
			cropped_image = image.crop((x, y, w+x, h+y))
			resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
			resized_image.save(to_change.avatar.path)

			output = BytesIO()
			resized_image.save(output, format='PNG', quality=85, optimize = True)
			output.seek(0)
			to_change.avatar = InMemoryUploadedFile(output, 'ImageField', "%s.png" %to_change.avatar.name, 'image/png', output.__sizeof__(), None)

		return to_change 
