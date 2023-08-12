from django.urls import path

from user_profile.views import (ProfileView, RegisterView, MyDeviceUser,
                                AcceptDeviceUser, AddDeviceUser, UploadPhotoView)
from device.views import DeviceAddListView, DeviceView
from app_week.views import AppWeekListAddView
from app_bin_core.views import ChangePasswordView

app_name = 'api'

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
    path('upload-photo/<pk>', UploadPhotoView.as_view(), name='upload-photo'),

    path('add-device', AddDeviceUser.as_view(), name='add-device'),
    path('my-device', MyDeviceUser.as_view(), name='my-device'),
    path('update-device/<pk>', AcceptDeviceUser.as_view(), name='update-device'),

    path('device-list', DeviceAddListView.as_view(), name='device-list'),
    path('device', DeviceView.as_view(), name='device'),

    path('app-week-list', AppWeekListAddView.as_view(), name='app-week-list'),

]
