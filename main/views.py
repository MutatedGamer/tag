from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from .models import *
from users.models import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import bleach
from main.forms import CustomGroupForm
from django.http import JsonResponse
from django.views import View
from django.template import loader
from django.db.models import Q
from django.db.models.functions import Concat
from django.db.models import Value

# Create your views here.

class ChangeOwnerSearch(View):
	template = 'main/change_owner_search_members.html'

	def post(self, request):
		template = loader.get_template(self.template)
		print(request.POST)
		query = request.POST.get('search', None)
		group = get_object_or_404(CustomGroup, pk=int(request.POST.get('group-id')))

		items= group.members.exclude(pk=group.owner.pk).annotate(full_name=Concat('first_name', Value(' '), 'last_name'))
		if query:
			items = items.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(full_name__icontains=query))

		context = {'query': query, 'members': items, 'admins': group.admins.all()}

		rendered_template = template.render(context, request)
		return HttpResponse(rendered_template, content_type='text/html')

class AddAdminSearch(ChangeOwnerSearch):
	template = 'main/manage_admins_search_members.html'


@csrf_protect
def index(request):
	context = dict()
	context['page'] = 'home'
	if request.user and not request.user.is_anonymous:
		posts = request.user.posts_to_show.all()
		for group in request.user.groups_in.all():
			posts = posts | group.posts.all()
		context['posts'] = posts.order_by('-added')
	return render(request, 'main/index.html', context)

@csrf_protect
def groups(request):
	context = dict()
	context['page'] = 'groups'
	if request.user.is_authenticated:
		context['groups_in'] = request.user.groups_in.all()
		context['groups'] = CustomGroup.objects.all().difference(context['groups_in']).order_by('-last_activity_date')
	else:
		context['groups'] = CustomGroup.objects.all().order_by('-last_activity_date')
	return render(request, 'main/groups.html', context)

@csrf_protect
def group(request, group_id):
	context = dict()
	context['page'] = 'groups'
	group = get_object_or_404(CustomGroup, pk=group_id)
	context['group' ] = group
	context['posts'] = group.posts.all().order_by('-added')
	context['members'] = group.members.all()
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
			group_form = CustomGroupForm(request.POST, request.FILES)
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
