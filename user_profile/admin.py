from django.contrib import admin
from .models import UserProfile, UserPairDevice

admin.site.register(UserProfile)
admin.site.register(UserPairDevice)