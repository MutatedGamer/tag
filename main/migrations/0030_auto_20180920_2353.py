# Generated by Django 2.1.1 on 2018-09-20 23:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_auto_20180920_2349'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['creation_date']},
        ),
    ]
