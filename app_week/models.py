from django.db import models
from device.models import Device
from datetime import datetime


class AppData(models.Model):
    device = models.ForeignKey(
        Device, related_name='my_device', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    app_name = models.CharField(max_length=50)
    package_name = models.CharField(max_length=80)
    hours = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    start_date = models.DateField(default=datetime.now, blank=True)
    end_date = models.DateField(default=datetime.now, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.start_date.strftime("%m/%d/%Y") + " - " + self.end_date.strftime("%m/%d/%Y")
