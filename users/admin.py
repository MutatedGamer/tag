from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = CustomUser
	list_display = ['email', 'username', 'uuid',]
	fieldsets = (
					(None, {
						'fields': ('username', 'password', 'uuid')
					}),
					('Personal info', {
						'fields': ('first_name', 'last_name', 'email',)
					}),
					('Permission', {
						'fields': ('is_active', 'is_staff', 'is_superuser', 'user_permissions',)
					}),
					('Important dates', {
						'fields': ('last_login', 'date_joined')
					}),
					('Other', {
						'fields': ('custom_groups', 'posts',)
					}),
				)

admin.site.register(CustomUser, CustomUserAdmin)
