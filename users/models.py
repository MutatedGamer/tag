from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUser(AbstractUser):
	uuid = models.CharField(max_length=40)
	custom_groups = models.ManyToManyField('main.CustomGroup', blank=True)
	posts_to_show = models.ManyToManyField('main.Post', symmetrical = False, blank=True)
	friends = models.ManyToManyField("self", blank=True)
	friend_requests_sent = models.ManyToManyField("self", blank=True, symmetrical = False, related_name = 'friend_requests_received')
	avatar = models.ImageField(upload_to='avatars/', default=None, null=True)


	def __str__(self):
		return self.email
