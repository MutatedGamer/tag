from django.db import models

# Create your models here.

class Post(models.Model):
	body = models.TextField()
	added = models.DateField(auto_now_add = True)

'''
class 'users.CustomUser'(AbstractUser):
	posts = models.ManyToManyField(Post)
	groups = models.ManyToManyField('Group')
	test = models.TextField()
	test2 = models.CharField(max_length = 20, default=None, blank = True, null = True)
'''

class CustomGroup(models.Model):
	name = models.CharField(max_length = 128)
	creation_date = models.DateField(auto_now_add = True)
	last_activity_date = models.DateTimeField(auto_now = True)
	posts = models.ManyToManyField(Post)
	admins = models.ManyToManyField('users.CustomUser')

