from django.db import models

# Create your models here.

class Post(models.Model):
	body = models.CharField(max_length = 5000)
	added = models.DateField(auto_now_add = True)
	group = models.ForeignKey('CustomGroup', on_delete = models.CASCADE, blank = True, null = True)

	class Meta:
		ordering = ['-added',]


class CustomGroup(models.Model):
	name = models.CharField(max_length = 128)
	creation_date = models.DateField(auto_now_add = True)
	moderated = models.BooleanField(default=False)
	last_activity_date = models.DateTimeField(auto_now = True)
	posts = models.ManyToManyField(Post, null=True)
	admins = models.ManyToManyField('users.CustomUser')
	owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name = 'groups_owned')
	photo = models.ImageField(upload_to='group_photos/', default=None, null=True)

	def __str__(self):
		return self.name

