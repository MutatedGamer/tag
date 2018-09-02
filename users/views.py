from django.shortcuts import render
from .models import CustomUser

# Create your views here.

def save_profile(backend, user, response, *args, **kwargs):
	if backend.name == 'facebook':
		sign_up = user
		sign_up.uuid = response.get('id')
		sign_up.save()
