# Generated by Django 2.1.1 on 2018-09-03 15:32

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20180902_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='custom_groups',
            field=models.ManyToManyField(null=True, to='main.CustomGroup'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='friend_requests_received',
            field=models.ManyToManyField(null=True, related_name='_customuser_friend_requests_received_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='friend_requests_sent',
            field=models.ManyToManyField(null=True, related_name='_customuser_friend_requests_sent_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='friends',
            field=models.ManyToManyField(null=True, related_name='_customuser_friends_+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='posts_to_show',
            field=models.ManyToManyField(null=True, to='main.Post'),
        ),
    ]
