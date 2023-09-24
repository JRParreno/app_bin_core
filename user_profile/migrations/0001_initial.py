# Generated by Django 4.1.7 on 2023-09-24 01:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='images/profiles/')),
                ('is_parent', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserPairDevice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_accepted', models.BooleanField(default=False)),
                ('user_pair', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_pair_device', to='user_profile.userprofile')),
                ('user_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_request_device', to='user_profile.userprofile')),
            ],
        ),
    ]
