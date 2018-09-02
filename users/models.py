from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUser(AbstractUser):
	test_text = models.TextField()
	uuid = models.CharField(max_length=40)
	custom_groups = models.ManyToManyField('main.CustomGroup')
	posts = models.ManyToManyField('main.Post')

	def __str__(self):
		return self.email
