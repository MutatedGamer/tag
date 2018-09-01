from django.shortcuts import render, HttpResponse

# Create your views here.

def index(request):
	context = dict()
	context['page'] = 'home'
	return render(request, 'main/index.html', context)

def groups(request):
	context = dict()
	context['page'] = 'groups'
	return render(request, 'main/groups.html', context)

def profile(request):
	context = dict()
	context['page'] = 'profile'
	return render(request, 'main/profile.html', context)
