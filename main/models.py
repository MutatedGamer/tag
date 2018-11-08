from django.db import models

# Create your models here.

class Post(models.Model):
    body = models.CharField(max_length = 5000)
    added = models.DateTimeField(auto_now_add = True)
    group = models.ForeignKey('CustomGroup', on_delete = models.CASCADE, blank = True, null = True)
    likes = models.IntegerField(default = 0)
    tag = models.ManyToManyField('users.CustomUser', related_name = 'tagged_in')
    reply_to = models.ForeignKey('Post', on_delete = models.CASCADE,
                                 blank=True, null = True, related_name =
                                 'replies')

    class Meta:
        ordering = ['added',]


class CustomGroup(models.Model):
    name = models.CharField(max_length = 128)
    creation_date = models.DateField(auto_now_add = True)
    moderated = models.BooleanField(default=False)
    last_activity_date = models.DateTimeField(auto_now = True)
    posts = models.ManyToManyField(Post, symmetrical = False)
    admins = models.ManyToManyField('users.CustomUser', related_name = 'groups_admin_of')
    owner = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name = 'groups_owned')
    photo = models.ImageField(upload_to='group_photos/', default=None, null=True)
    members = models.ManyToManyField('users.CustomUser', related_name = 'groups_in')
    to_approve = models.ManyToManyField(Post, symmetrical = False, related_name = 'posts_to_approve')


    def __str__(self):
        return self.name


class Notification(models.Model):
    sender = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, blank = True, null = True, related_name = 'notifications_sent')
    receiver = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name = 'notifications')
    action = models.CharField(max_length=50, blank=True, null=True)
    read = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add = True)
    for_group = models.ForeignKey(CustomGroup, on_delete=models.CASCADE, blank = True, null = True)
    for_post = models.ForeignKey(Post, on_delete=models.CASCADE, blank = True, null = True)

    def __str__(self):
        return self.action + ' to ' + str(self.receiver)

    class Meta:
        ordering = ['-creation_date']

class Comment(models.Model):
    poster = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name = 'comments')
    creation_date = models.DateTimeField(auto_now_add = True)
    body = models.CharField(max_length = 2500, blank = True, default = None, null = True)
    
    class Meta:
        ordering = ['-creation_date',]
