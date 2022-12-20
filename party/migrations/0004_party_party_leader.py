# Generated by Django 4.1.2 on 2022-11-15 01:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('party', '0003_alter_party_invites'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='party_leader',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='party_leader', to=settings.AUTH_USER_MODEL),
        ),
    ]