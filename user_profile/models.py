from django.db import models
from django.contrib.auth.models import User
from app_bin_core import settings


class UserProfile(models.Model):
    class ProfileManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().select_related('user')

    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)

    profile_photo = models.ImageField(
        upload_to='images/profiles/', blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.last_name} - {self.user.first_name}'


class UserPairDevice(models.Model):

    user_request = models.ForeignKey(UserProfile, related_name='user_request_device', on_delete=models.CASCADE)

    user_pair = models.ForeignKey(UserProfile, related_name='user_pair_device',on_delete=models.CASCADE)

    is_accepted = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user_request.user.last_name} - {self.user_request.user.first_name}'