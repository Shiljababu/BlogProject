# Generated by Django 5.0.6 on 2024-08-07 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminpanel', '0008_alter_blog_blog_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(default='visible', max_length=20),
        ),
    ]
