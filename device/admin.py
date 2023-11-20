from django.contrib import admin
from .models import Device, DeviceApp, BlockSchedule

admin.site.register(Device)
admin.site.register(DeviceApp)
admin.site.register(BlockSchedule)
