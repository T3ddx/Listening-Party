# Generated by Django 4.1.2 on 2022-10-27 03:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_users_logged_in'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='logged_in',
        ),
    ]