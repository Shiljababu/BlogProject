# Generated by Django 5.0.6 on 2024-07-27 14:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Blog_Table',
            new_name='Blog',
        ),
        migrations.RenameModel(
            old_name='Comment_Table',
            new_name='Comment',
        ),
    ]
