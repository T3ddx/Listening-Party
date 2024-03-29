# Generated by Django 4.1.1 on 2022-12-24 00:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('party', '0005_alter_party_party_leader'),
    ]

    operations = [
        migrations.CreateModel(
            name='Party_Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('in_party', models.BooleanField(blank=True, default=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='party_member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='party',
            name='party_leader',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='party_leader', to='party.party_member'),
        ),
        migrations.AlterField(
            model_name='party',
            name='users',
            field=models.ManyToManyField(blank=True, to='party.party_member'),
        ),
    ]
