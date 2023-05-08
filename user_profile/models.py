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
    parent_user = models.ForeignKey(User, related_name='parent_user', 
                                    on_delete=models.SET_NULL ,null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.last_name} - {self.user.first_name}'
