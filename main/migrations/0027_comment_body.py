# Generated by Django 2.1.1 on 2018-09-20 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_auto_20180920_1443'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='body',
            field=models.CharField(blank=True, default=None, max_length=2500, null=True),
        ),
    ]
