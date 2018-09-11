from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from users.models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import bleach
from users.forms import CustomUserEditProfileForm
from main.forms import CustomGroupForm
from django.http import JsonResponse
from django.views import View
from django.template import loader
from django.db.models import Q
from django.db.models.functions import Concat
from django.db.models import Value
from datetime import datetime
from django.utils.decorators import method_decorator
import requests
import json


# Create your views here.

class ChangeOwnerSearch(View):
	template = 'main/change_owner_search_members.html'

	@method_decorator(login_required)
	def post(self, request):
		template = loader.get_template(self.template)
		query = request.POST.get('search', None)
		group = get_object_or_404(CustomGroup, pk=int(request.POST.get('group-id')))

		items= group.members.exclude(pk=group.owner.pk).annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
		if query:
			items = items.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(full_name__icontains=query))

		context = {'query': query, 'members': items, 'admins': group.admins.all()}

		rendered_template = template.render(context, request)
		return HttpResponse(rendered_template, content_type='text/html')

class InviteMemberSearch(View):
	template = 'main/search_invite_member.html'

	@method_decorator(login_required)
	def post(self, request):
		template = loader.get_template(self.template)
		query = request.POST.get('search', None)
		group = get_object_or_404(CustomGroup, pk=int(request.POST.get('group-id')))

		items= request.user.friends.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
		if query:
			items = items.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(full_name__icontains=query))
		items = items.difference(group.members.annotate(full_name=Concat('first_name', Value(' '), 'last_name')).all())

		context = {'friends': items}

		rendered_template = template.render(context, request)
		return HttpResponse(rendered_template, content_type='text/html')


class AddAdminSearch(ChangeOwnerSearch):
	template = 'main/manage_admins_search_members.html'

class GetNotifications(View):
	template = 'main/get_notifications.html'

	@method_decorator(login_required)
	def get(self, request):
		context = dict()
		context['page'] = 'notifications'
		context['notifications'] = request.user.notifications.all()
		return render(request, 'main/notifications.html', context)


	@method_decorator(login_required)
	def post(self, request):
		template = loader.get_template(self.template)
		items = request.user.notifications.all()
		context = {'items': items}

		rendered_template = template.render(context, request)
		return HttpResponse(rendered_template, content_type='text/html')

class TagFriends(View):
	template = 'main/search_tag_friends.html'

	@method_decorator(login_required)
	def post(self, request):
		template = loader.get_template(self.template)
		post = get_object_or_404(Post, pk=int(request.POST['post-id']))
		items= request.user.friends.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
		query = request.POST.get('search', None)
		if query:
			items = items.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(full_name__icontains=query))
		items = items.difference(post.tag.annotate(full_name=Concat('first_name', Value(' '), 'last_name')).all())
		context = {'friends': items, 'post': post}

		rendered_template = template.render(context, request)
		return HttpResponse(rendered_template, content_type='text/html')


@csrf_protect
@login_required
def tag(request):
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('index'))
	
	post = get_object_or_404(Post, pk=int(request.POST['post-id']))
	tagged_friend = get_object_or_404(CustomUser, pk=int(request.POST['friend-pk']))

	# Tag friend if not already tagged
	if tagged_friend not in post.tag.all():
		post.tag.add(tagged_friend)
		post.save()
	else:
		messages.error(request, 'User is already tagged')
		return HttpResponseRedirect(reverse('index'))
	
	# Create notification
	notification = Notification(sender = request.user, receiver = tagged_friend, action = 'tagged', for_post = post)
	notification.save()
	return JsonResponse({'success': True})


@csrf_protect
@login_required
def star(request):
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('index'))
	
	post = get_object_or_404(Post, pk=int(request.POST['post-id']))

	
	if post not in request.user.starred_posts.all():
		request.user.starred_posts.add(post)
		post.save()
		result = 'starred'
		print('starred')
	else:
		request.user.starred_posts.remove(post)
		post.save()
		result = 'disliked'
	
	return JsonResponse({'result': result})


@csrf_protect
@login_required
def invite_member(request, group_id):
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('index'))
	
	group = get_object_or_404(CustomGroup, pk=group_id)
	invited_user = get_object_or_404(CustomUser, pk=int(request.POST['friend-pk']))

	if request.user not in group.members.all():
		return HttpResponseRedirect(reverse('index'))

	# Tag friend if not already tagged
	if invited_user not in group.members.all():
		notification, created = Notification.objects.get_or_create(sender = request.user, receiver = invited_user, action="invited", for_group = group)
		notification.save()
	else:
		messages.error(request, 'User is already in group')
		return HttpResponseRedirect(reverse('index'))
	
	return JsonResponse({'success': True})


@csrf_protect
def index(request):
	context = dict()
	context['page'] = 'home'
	if request.user and not request.user.is_anonymous:
		posts = request.user.posts_to_show.all()
		context['liked_posts'] = request.user.liked_posts.all()
		for group in request.user.groups_in.all():
			posts = posts | group.posts.all()
		posts = posts.order_by('-added')
		page = request.GET.get('page', 1)
		paginator = Paginator(posts, 3)
		try:
			posts = paginator.page(page)
		except PageNotAnInteger:
			posts = paginator.page(1)
		except EmptyPage:
			posts = paginator.page(paginator.num_pages)
		context['posts'] = posts

		social_user = request.user.social_auth.filter(provider = 'facebook').first()
		if social_user:
			url = u'https://graph.facebook.com/{0}/friends?fields=id,name&access_token={1}'.format(social_user.uid, social_user.extra_data['access_token'],)
			content = requests.get(url)
			friends = json.loads(content.content.decode('utf-8'))['data']
			context['suggested_friends'] = []

			for friend in friends:
				found_friend = CustomUser.objects.get(uuid=friend['id'])
				if found_friend not in request.user.friends.all() and found_friend not in request.user.friend_requests_sent.all() and found_friend not in request.user.friend_requests_received.all():
					context['suggested_friends'] += [found_friend]

		# Get suggested groups
		context['suggested_groups'] = request.user.groups_in.all() 
		for friend in request.user.friends.all():
			context['suggested_groups'] = context['suggested_groups'] | friend.groups_in.all()
		context['suggested_groups'] = context['suggested_groups'].difference(request.user.groups_in.all())
	return render(request, 'main/index.html', context)

@login_required
@csrf_protect
def edit_profile(request):
	if request.method == 'POST':
		bio  = bleach.clean(request.POST['bio'])

		school = bleach.clean(request.POST['school'])

		form = CustomUserEditProfileForm({'school': school, 'bio': bio}, request.FILES, instance=request.user)

		if form.is_valid():
			edit = form.save(commit = False)
			edit.save()
			return HttpResponseRedirect(reverse('user-profile', args=(request.user.pk,)))



def post(request, post_id):
	context = dict()
	context['page'] = 'groups'
	post = Post.objects.filter(pk=post_id)
	context['posts'] = post

	return render(request, 'main/post.html', context)

@csrf_protect
def groups(request):
	context = dict()
	context['page'] = 'groups'
	if request.user.is_authenticated:
		context['groups_in'] = request.user.groups_in.all()
		context['groups'] = CustomGroup.objects.all().difference(context['groups_in']).order_by('-last_activity_date')
		# Get suggested groups
		context['suggested_groups'] = request.user.groups_in.all() 
		for friend in request.user.friends.all():
			context['suggested_groups'] = context['suggested_groups'] | friend.groups_in.all()
		context['suggested_groups'] = context['suggested_groups'].difference(request.user.groups_in.all())

	else:
		context['groups'] = CustomGroup.objects.all().order_by('-last_activity_date')
	return render(request, 'main/groups.html', context)

@csrf_protect
def group(request, group_id):
	context = dict()
	context['page'] = 'groups'
	group = get_object_or_404(CustomGroup, pk=group_id)
	context['group' ] = group
	posts = group.posts.all().order_by('-added')
	page = request.GET.get('page', 1)
	paginator = Paginator(posts, 3)
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)
	context['posts'] = posts

	context['members'] = group.members.all()
	context['liked_posts'] = request.user.liked_posts.all()
	if request.user.is_authenticated:
		if request.user == group.owner:
			context['is_owner'] = True
		else:
			context['is_owner'] = False
		
		if request.user in group.admins.all():
			context['is_admin'] = True
		else:
			context['is_admin'] = False

		if request.user in group.members.all():
			context['is_member'] = True
		else:
			context['is_member'] = False

	return render(request, 'main/group.html', context)

def submit_post(request, group, post):
	if post in group.to_approve.all():
		group.to_approve.remove(post)
	group.posts.add(post)
	return

@csrf_protect
@login_required
def like(request):
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('index'))
	
	post = get_object_or_404(Post, pk=int(request.POST['post-id']))

	
	if post not in request.user.liked_posts.all():
		request.user.liked_posts.add(post)
		post.likes = post.likes + 1
		post.save()
		result = 'liked'
	else:
		request.user.liked_posts.remove(post)
		post.likes = post.likes - 1
		post.save()
		result = 'disliked'
	
	return JsonResponse({'result': result, 'new_count':post.likes})



@csrf_protect
@login_required
def submit_post_to_group(request, group_id):
	if request.method == 'POST':
		group = get_object_or_404(CustomGroup, pk=group_id)
		if group.pk != int(request.POST['group_id']):
			messages.error(request, 'Something went wrong')
			return HttpResponseRedirect(reverse('index'))

		if request.user not in group.members.all():
			messages.error(request, "You cannot post in groups you are not a part of.")
			return HttpResponseRedirect(reverse('index'))

		post = Post(body = bleach.clean(request.POST['body']), group=group)
		post.save()
		
		if group.moderated:
			group.to_approve.add(post)
			group.save()
			messages.success(request, "Your post was submitted to be approved!")
			# create notification for all admins
			for admin in group.admins.all():
				notification, created  = Notification.objects.get_or_create(
					for_group = group,
					receiver = admin,
					action = 'posts_to_approve',
				)
				if not created:
					notification.read = False
					notification.creation_date = datetime.now()
					notification.save()

			return HttpResponseRedirect(reverse('group', args=(group.pk,)))
		else:
			group.posts.add(post)
			group.save()
			messages.success(request, "Your post was submitted successfully!")
			return HttpResponseRedirect(reverse('group', args=(group.pk,)))

@csrf_protect	
@login_required
def approve_posts(request, group_id):
	group = get_object_or_404(CustomGroup, pk=group_id)
	context = dict()
	context['page'] = 'groups'
	if not request.user in group.admins.all():
		messages.error(request, "Only admins can approve posts.")
		return HttpResponseRedirect(reverse('index'))
	# Set notificaiton to read
	notification = Notification.objects.get(for_group = group, receiver = request.user, action="posts_to_approve")
	notification.read = True
	notification.save()
	context = dict()
	context['group'] = group
	context['posts'] = group.to_approve.all()
	return render(request, 'main/approve.html', context)

@csrf_protect
@login_required
def approve_posts_response(request, group_id):
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('index'))

	group = get_object_or_404(CustomGroup, pk=group_id)
	if not request.user in group.admins.all():
		messages.error(request, "Only admins can approve posts.")
		return HttpResponseRedirect(reverse('index'))

	post = get_object_or_404(Post, pk=int(request.POST['post-id']))
	if post not in group.to_approve.all():
		messages.error(request, "Post not found.")
		return HttpResponseRedirect(reverse('index'))

	if 'approve' in request.POST:
		group.to_approve.remove(post)
		group.posts.add(post)
		group.save()
		response = {'result': 'approved'}
	elif 'remove' in request.POST:
		group.to_approve.remove(post)
		group.save()
		response = {'result': 'deleted'}
	
	return JsonResponse(response)

@csrf_protect
@login_required
def change_group_owner(request, group_id):
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('index'))
	if int(request.POST['group']) != group_id:
		return HttpResponseRedirect(reverse('index'))

	group = get_object_or_404(CustomGroup, pk=group_id)

	if request.user != group.owner:
		messages.error(request, 'Only the owner can change the owner.')
		return HttpResponseRedirect(reverse('index'))
	
	new_owner = get_object_or_404(CustomUser, pk=int(request.POST['user-id']))
	group.owner = new_owner
	if new_owner not in group.admins.all():
		group.admins.add(new_owner)
	group.save()

	return JsonResponse({'success': True})

@csrf_protect
@login_required
def add_admin(request, group_id):
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('index'))
	if int(request.POST['group']) != group_id:
		return HttpResponseRedirect(reverse('index'))

	group = get_object_or_404(CustomGroup, pk=group_id)

	if request.user != group.owner:
		messages.error(request, 'Only the owner can modify admins.')
		return HttpResponseRedirect(reverse('index'))
	
	new_admin = get_object_or_404(CustomUser, pk=int(request.POST['user-id']))
	if new_admin not in group.admins.all():
		group.admins.add(new_admin)
	group.save()

	return JsonResponse({'success': True})

@csrf_protect
@login_required
def remove_admin(request, group_id):
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('index'))
	if int(request.POST['group']) != group_id:
		return HttpResponseRedirect(reverse('index'))

	group = get_object_or_404(CustomGroup, pk=group_id)

	if request.user != group.owner:
		messages.error(request, 'Only the owner can modify admins.')
		return HttpResponseRedirect(reverse('index'))
	
	to_remove = get_object_or_404(CustomUser, pk=int(request.POST['user-id']))
	if to_remove in group.admins.all():
		group.admins.remove(to_remove)
	group.save()

	return JsonResponse({'success': True})

@csrf_protect
@login_required
def delete_group(request, group_id):
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('index'))
	if int(request.POST['group']) != group_id:
		return HttpResponseRedirect(reverse('index'))

	group = get_object_or_404(CustomGroup, pk=group_id)

	if request.user != group.owner:
		messages.error(request, 'Only the owner can remove a group.')
		return HttpResponseRedirect(reverse('index'))

	group.delete()

	return JsonResponse({'success': True})

@csrf_protect
@login_required
def make_group_unmoderated(request, group_id):
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('index'))
	if int(request.POST['group']) != group_id:
		return HttpResponseRedirect(reverse('index'))

	group = get_object_or_404(CustomGroup, pk=group_id)

	if request.user != group.owner:
		messages.error(request, 'Only the owner can make the group unmoderated.')
		return HttpResponseRedirect(reverse('index'))

	group.moderated = False
	for post in group.to_approve.all():
		group.to_approve.remove(post)
		group.posts.add(post)
	group.save()

	Notification.objects.get(for_group=group).delete()

	return JsonResponse({'success': True})



		

@login_required
def join_group(request, group_id):
	group = get_object_or_404(CustomGroup, pk=group_id)
	if request.user.is_authenticated and request.user not in group.members.all():
		group.members.add(request.user)
	
	return HttpResponseRedirect(reverse('group', args=(group.pk,)))

@login_required
def leave_group(request, group_id):
	group = get_object_or_404(CustomGroup, pk=group_id)
	if request.user == group.owner:
		messages.error(request, 'You cannot leave a group you are the owner of.')
		return HttpResponseRedirect(reverse('group', args=(group.pk,)))
	if request.user.is_authenticated and request.user in group.members.all():
		group.members.remove(request.user)
		if request.user in group.admins.all():
			group.admins.remove(request.user)
		group.save()
	
	return HttpResponseRedirect(reverse('group', args=(group.pk,)))

def profile(request):
	context = dict()
	context['page'] = 'profile'
	if request.user.is_authenticated:
		context['posts'] = request.user.starred_posts.all().order_by('-added')
	return render(request, 'main/profile.html', context)

@login_required
@csrf_protect
def create_group(request):
	if request.method == 'POST':
		group_name = request.POST['name']
		group_name = bleach.clean(group_name)
		moderated = request.POST['moderated']
		moderated = bleach.clean(moderated)
		if CustomGroup.objects.filter(name = group_name).count() > 0:
			messages.error(request, "A group with that name already exists. Sorry!")
			return HttpResponseRedirect(reverse('groups') + '#create-group')
		else:
			group_form = CustomGroupForm({'name': group_name, 'moderated': moderated}, request.FILES)
			# group = CustomGroup(name=group_name, owner=request.user)
			if group_form.is_valid():
				group = group_form.save(commit = False)
				group.owner = request.user
				group.save()
				group.admins.add(request.user)
				group.members.add(request.user)
				group.save()
				return HttpResponseRedirect(reverse('group', args=(group.pk,)))
			else:
				messages.error(request, "Form wasn't valid!")
				return HttpResponseRedirect(reverse('groups') + '#create-group')

@csrf_protect
def user_profile(request, user_id):
	userProfile = get_object_or_404(CustomUser, pk=user_id)
	context = dict()
	context['page'] = 'profile'

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
def send_friend_request(request, user_id):
	# The user receiving the friend request
	userProfile = get_object_or_404(CustomUser, pk=user_id)
	if userProfile in request.user.friend_requests_sent.all():
		messages.error('Something went wrong')
		return HttpResponseRedirect(reverse('index'))
	# Add to the logged in user's list of friend requests sent.
	# Automatically adds logged in user to list of friend requests received
	# for userProfile
	request.user.friend_requests_sent.add(userProfile)
	
	# Create a new notification for userProfile
	friend_request_notification = Notification(sender=request.user, receiver=userProfile, action='friend_request_received')
	friend_request_notification.save()

	return HttpResponseRedirect(reverse('user-profile', args=(userProfile.pk,)))

@csrf_protect
@login_required
def remove_friend(request, user_id):
	userProfile = get_object_or_404(CustomUser, pk=user_id)

	if userProfile not in request.user.friends.all():
		messages.error('Friend not found')
		return HttpResponseRedirect(reverse('index'))
	
	request.user.friends.remove(userProfile)
	request.user.save()

	return HttpResponseRedirect(reverse('user-profile', args=(userProfile.pk,)))

@csrf_protect
@login_required
def respond_to_friend_request(request, user_id):

	userProfile = get_object_or_404(CustomUser, pk=user_id)

	# Remove notification
	notification = Notification.objects.get(receiver=request.user, sender=userProfile, action="friend_request_received")
	notification.delete()
	
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
