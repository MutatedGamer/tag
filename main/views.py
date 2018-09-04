from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from .models import *
from users.models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import bleach
from main.forms import CustomGroupForm

# Create your views here.

@csrf_protect
def index(request):
	context = dict()
	context['page'] = 'home'
	if request.user and not request.user.is_anonymous:
		context['posts'] = request.user.posts_to_show.all()
	return render(request, 'main/index.html', context)

@csrf_protect
def groups(request):
	context = dict()
	context['page'] = 'groups'
	return render(request, 'main/groups.html', context)

def profile(request):
	context = dict()
	context['page'] = 'profile'
	return render(request, 'main/profile.html', context)

@login_required
@csrf_protect
def create_group(request):
	if request.method == 'POST':
		group_name = request.POST['name']
		group_name = bleach.clean(group_name)
		if CustomGroup.objects.filter(name = group_name).count() > 0:
			messages.error(request, "A group with that name already exists. Sorry!")
			return HttpResponseRedirect(reverse('groups') + '#create-group')
		else:
			print(request.POST)
			group_form = CustomGroupForm(request.POST, request.FILES)
			# group = CustomGroup(name=group_name, owner=request.user)
			if group.is_valid():
				group = group_form.save(commit = False)
				group.owner = request.user
				group.save()
				group.admins.add(request.user)
				group.save()
				return HttpResponseRedirect(reverse('groups'))
			else:
				messages.error(request, "Form wasn't valid!")
				return HttpResponseRedirect(reverse('groups') + '#create-group')

@csrf_protect
def user_profile(request, user_id):
	userProfile = get_object_or_404(CustomUser, pk=user_id)
	context = dict()

	if userProfile in request.user.friends.all():
		context['is_friend'] = True
	else:
		context['is_friend'] = False


	if userProfile in request.user.friend_requests_sent.all():
		context['sent_request'] = True
	else:
		context['sent_request'] = False


	if userProfile in request.user.friend_requests_received.all():
		context['received_request'] = True
	else:
		context['received_request'] = False

	context['userProfileFriends'] = userProfile.friends.all()
	context['userProfile'] = userProfile

	return render(request, 'main/user.html', context)

@csrf_protect
@login_required
def send_request(request, user_id):
	userProfile = get_object_or_404(CustomUser, pk=user_id)
	request.user.friend_requests_sent.add(userProfile)

	return HttpResponseRedirect(reverse('user-profile', args=(userProfile.pk,)))

@csrf_protect
@login_required
def respond_request(request, user_id):
	userProfile = get_object_or_404(CustomUser, pk=user_id)
	
	# Check if userProfile added request.user
	if userProfile not in request.user.friend_requests_received.all():
		messages.error(request, "Something went wrong responding to a friend request...")
		return HttpResponseRedirect(reverse('index'))

	# If yes, then add to friends and remove from request
	if 'accept' in request.POST:
		# if accepting, add friend
		request.user.friends.add(userProfile)
	request.user.friend_requests_received.remove(userProfile)
	return HttpResponseRedirect(reverse('user-profile', args=(userProfile.pk,)))

@csrf_protect
@login_required
def submit_post(request):
	if request.method == 'POST':
		body = bleach.clean(request.POST['body'])

		# Make a new post object
		post = Post(body = body)
		post.save()

		# Check if we're not in a group
		if 'group-name' not in request.POST:
			# show it to the author
			request.user.posts_to_show.add(post)

			# show it to all of the poster's friends
			for friend in request.user.friends.all():
				friend.posts_to_show.add(post)


		# return to index
		return HttpResponseRedirect(reverse('index'))
