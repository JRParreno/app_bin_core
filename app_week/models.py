from django.db import models
from  device.models import Device

class AppWeek(models.Model):
    device = models.ForeignKey(Device, related_name='my_device', on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.start_date.strftime("%m/%d/%Y, %H:%M:%S") + " - " + self.end_date.strftime("%m/%d/%Y, %H:%M:%S")