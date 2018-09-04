from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('', views.index, name="index"),
	path('login', auth_views.LoginView.as_view(template_name="registration/login.html"), name='login'),
	path('logout', auth_views.LogoutView.as_view(), name='logout'),
	path('oath/', include('social_django.urls', namespace='social')),
	path('groups', views.groups, name='groups'),
	path('profile', views.profile, name='profile'),
	path('create-group', views.create_group, name='create-group'),
	path('user/<int:user_id>', views.user_profile, name='user-profile'),
	path('user/<int:user_id>/send-request', views.send_request, name="send-request"),
	path('user/<int:user_id>/respond-request', views.respond_request, name="respond-request"),
	path('submit-post', views.submit_post, name='submit-post'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
