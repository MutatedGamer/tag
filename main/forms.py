from django import forms
from PIL import Image
from django.core.files import File
from main.models import CustomGroup
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

class CustomGroupForm(forms.ModelForm):
	x = forms.FloatField(widget=forms.HiddenInput())
	y = forms.FloatField(widget=forms.HiddenInput())
	width = forms.FloatField(widget=forms.HiddenInput())
	height = forms.FloatField(widget=forms.HiddenInput())

	class Meta:
		model = CustomGroup
		fields = ('name', 'moderated',  'photo', 'x', 'y', 'width', 'height',)

	def save(self, **kwargs):
		to_change = super(CustomGroupForm, self).save(commit = False)


		x = self.cleaned_data.get('x')
		y = self.cleaned_data.get('y')
		w = self.cleaned_data.get('width')
		h = self.cleaned_data.get('height')

		image = Image.open(to_change.photo)
		cropped_image = image.crop((x, y, w+x, h+y))
		resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
		resized_image.save(to_change.photo.path)

		output = BytesIO()
		resized_image.save(output, format='PNG', quality=85, optimize = True)
		output.seek(0)
		to_change.photo = InMemoryUploadedFile(output, 'ImageField', "%s.png" %to_change.photo.name, 'image/png', output.__sizeof__(), None)

		return to_change 
