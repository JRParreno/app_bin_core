import json
from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import User
from app_bin_core import settings
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification


class UserProfile(models.Model):
    class ProfileManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().select_related('user')

    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)

    profile_photo = models.ImageField(
        upload_to='images/profiles/', blank=True, null=True)
    is_parent = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.last_name} - {self.user.first_name}'


class UserPairDevice(models.Model):

    P = 'PENDING'
    A = 'ACCEPTED'
    R = 'REJECTED'

    PAIR_STATUS_CHOICES = [
        (P, 'PENDING'),
        (A, 'ACCEPTED'),
        (R, 'REJECTED'),
    ]

    user_request = models.ForeignKey(
        UserProfile, related_name='user_request_device', on_delete=models.CASCADE)

    user_pair = models.ForeignKey(
        UserProfile, related_name='user_pair_device', on_delete=models.CASCADE)

    pair_status = models.CharField(
        choices=PAIR_STATUS_CHOICES, default=P, max_length=100)

    def __str__(self):
        return f'{self.user_request.user.last_name} - {self.user_request.user.first_name}'

    def save(self, *args, **kwargs):
        body = f"App Bin Apps "

        if self.pair_status == 'PENDING':
            body += f"{self.user_request.user.get_full_name()} is requesting to view your data as parent"
            devices = FCMDevice.objects.filter(
                user=self.user_pair.user)

            for device in devices:
                data = {
                    "title": "AppBinApps",
                    "body": body,
                    "pair_status": self.pair_status,
                    "pk": str(self.pk)
                }
                device.send_message(
                    Message(
                        notification=Notification(
                            title=self.pair_status, body=body
                        ),
                        data={
                            "json": json.dumps(data)
                        },
                    )
                )
        elif self.pair_status == 'ACCEPTED':
            print("Notify user request accepted")
        else:
            print("Notify user rejected")

        super(UserPairDevice, self).save(*args, **kwargs)
