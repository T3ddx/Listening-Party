# Generated by Django 4.1.2 on 2022-10-21 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0002_remove_users_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='friends',
        ),
    ]
