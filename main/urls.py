from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static
from main.views import ChangeOwnerSearch, AddAdminSearch

urlpatterns = [
	path('', views.index, name="index"),
	path('login', auth_views.LoginView.as_view(template_name="registration/login.html"), name='login'),
	path('logout', auth_views.LogoutView.as_view(), name='logout'),
	path('oath/', include('social_django.urls', namespace='social')),
	path('groups', views.groups, name='groups'),
	path('profile', views.profile, name='profile'),
	path('search/change-group-owner-search', ChangeOwnerSearch.as_view(), name='change-group-owner-search'),
	path('search/add-admin-search', AddAdminSearch.as_view(), name='add-admin-search'),
	path('create-group', views.create_group, name='create-group'),
	path('user/<int:user_id>', views.user_profile, name='user-profile'),
	path('user/<int:user_id>/send-request', views.send_request, name="send-request"),
	path('user/<int:user_id>/respond-request', views.respond_request, name="respond-request"),
	path('submit-post', views.submit_post, name='submit-post'),
	path('group/<int:group_id>', views.group, name='group'),
	path('group/<int:group_id>/add_admin', views.add_admin, name='add-admin'),
	path('group/<int:group_id>/remove_admin', views.remove_admin, name='remove-admin'),
	path('group/<int:group_id>/join', views.join_group, name='join-group'),
	path('group/<int:group_id>/leave', views.leave_group, name='leave-group'),
	path('group/<int:group_id>/submit', views.submit_post_to_group, name='submit-post-to-group'),
	path('group/<int:group_id>/approve', views.approve_posts, name='approve-posts'),
	path('group/<int:group_id>/approve/respond', views.approve_posts_response, name="group-approve-response"),
	path('group/<int:group_id>/delete', views.delete_group, name='delete-group'),
	path('group/<int:group_id>/change-owner', views.change_group_owner, name="change-group-owner"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)