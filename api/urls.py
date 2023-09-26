from django.urls import path
from django.contrib.auth import views as auth_views
from api.views import RequestPasswordResetEmail

from user_profile.views import (ProfileView, RegisterView, MyDeviceUser,
                                AcceptDeviceUser, AddDeviceUser, UploadPhotoView)
from device.views import DeviceAddListView, DeviceView, ViewAllUserDevices
from app_week.views import AppDataListAddView
from app_bin_core.views import ChangePasswordView

app_name = 'api'

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('change-password', ChangePasswordView.as_view(), name='change-password'),
    path('upload-photo/<pk>', UploadPhotoView.as_view(), name='upload-photo'),

    path('forgot-password', RequestPasswordResetEmail.as_view(),
         name='forgot-password '),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),

    path('add-device', AddDeviceUser.as_view(), name='add-device'),
    path('my-device', MyDeviceUser.as_view(), name='my-device'),
    path('update-device/<pk>', AcceptDeviceUser.as_view(), name='update-device'),
    path('view-user-all-device', ViewAllUserDevices.as_view(),
         name='view-user-all-device'),

    path('device-list', DeviceAddListView.as_view(), name='device-list'),
    path('device', DeviceView.as_view(), name='device'),
    path('app-data-list', AppDataListAddView.as_view(), name='app-data-list'),

]
