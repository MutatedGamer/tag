# Generated by Django 2.1.1 on 2018-09-11 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_customuser_starred_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bio',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='customuser',
            name='school',
            field=models.CharField(default='', max_length=120),
        ),
    ]
