from django.db import models
from django.contrib.auth.models import User
from user_profile.models import UserProfile


class Device(models.Model):
    user_profile = models.ForeignKey(
        UserProfile, related_name='device_profile', on_delete=models.CASCADE)
    device_name = models.CharField(max_length=50)
    device_code = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user_profile.user.username} {self.device_name}'


class DeviceApp(models.Model):
    device = models.ForeignKey(
        Device, related_name='my_device_app', on_delete=models.CASCADE)
    app_name = models.CharField(max_length=50)
    package_name = models.CharField(max_length=80)
    is_block = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.app_name} : {self.device.device_name} - {self.is_block}'


class BlockSchedule(models.Model):
    device = models.ForeignKey(
        Device, related_name='my_device_app_block', on_delete=models.CASCADE)
    my_date_time = models.DateTimeField(blank=False, null=False)
    is_hourly = models.BooleanField(default=False)
    hours = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.device.device_name} - {self.is_hourly}'
