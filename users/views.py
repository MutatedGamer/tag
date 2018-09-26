from django.shortcuts import render
from .models import CustomUser
from requests import request, HTTPError
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
from main.models import CustomGroup

# Create your views here.

def save_profile(backend, user, response, *args, **kwargs):
	if backend.name == 'facebook':
		sign_up = user
		sign_up.uuid = response.get('id')
		sign_up.save()
		if not sign_up.avatar:
			# Add new users to tag@mit group
			try:
				group = CustomGroup.objects.get(name="tag@mit")
				group.members.add(sign_up)
				group.save()
			except ObjectDoesNotExist:
				pass
			url = 'https://graph.facebook.com/{0}/picture'.format(response['id'])
			try:
				response = request('GET', url, params={'type': 'large'})
				response.raise_for_status()
			except:
				pass
			else:
				sign_up.avatar.save('profile_pic_{}.jpg'.format(user.username), ContentFile(response.content))
				sign_up.save() 
