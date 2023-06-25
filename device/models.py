from django.db import models
from django.contrib.auth.models import User
from user_profile.models import UserProfile

class Device(models.Model):
    user_profile = models.ForeignKey(UserProfile, related_name='device_profile', on_delete=models.CASCADE)
    device_name = models.CharField(max_length=50, unique=True)
    device_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.user_profile.user.username} {self.device_name}'
