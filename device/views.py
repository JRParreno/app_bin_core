from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets, permissions, generics, response

from api.paginate import ExtraSmallResultsSetPagination
from .serializers import DeviceSerializer, DeviceAppSerializer
from .models import Device, DeviceApp
from user_profile.models import UserProfile


class DeviceAddListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeviceSerializer
    queryset = Device.objects.all().order_by('device_name')
    pagination_class = ExtraSmallResultsSetPagination

    def get_queryset(self):
        queryset = Device.objects.all().order_by('device_name')

        user_profiles = UserProfile.objects.filter(
            user__pk=self.request.user.pk)
        if user_profiles.exists():
            user_profile = user_profiles.first()
            return Device.objects.filter(user_profile=user_profile).order_by(
                'device_name')

        return queryset

    def post(self, request, *args, **kwargs):
        device_code = request.data.get('device_code')
        device_name = request.data.get('device_name')

        user_profile = UserProfile.objects.get(user__pk=self.request.user.pk)

        check_device_exists = Device.objects.filter(
            device_code=device_code, user_profile=user_profile).exists()

        if not check_device_exists:

            user_profile = UserProfile.objects.get(
                user__pk=self.request.user.pk)

            device = Device.objects.create(
                user_profile=user_profile,
                device_code=device_code,
                device_name=device_name,
            )

            data = {
                "pk": device.pk,
                "device_name": device.device_name,
                "device_code": device.device_code
            }

            return response.Response(data, status=status.HTTP_200_OK)

        error = {
            "error_message": "Device Already Exists"
        }
        return response.Response(error, status=status.HTTP_400_BAD_REQUEST)


class DeviceView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeviceSerializer
    queryset = Device.objects.all().order_by('device_name')
    pagination_class = ExtraSmallResultsSetPagination

    def get_queryset(self):
        q = self.request.query_params.get('q', None)
        user_profile = UserProfile.objects.get(
            user__pk=self.request.user.pk)
        queryset = Device.objects.filter(
            device_code=q, user_profile=user_profile).order_by('device_name')

        return queryset


class ViewAllUserDevices(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeviceSerializer
    queryset = Device.objects.all().order_by('device_name')

    def get_queryset(self):
        q = self.request.query_params.get('q', None)
        device_code = self.request.query_params.get('device_code', None)

        queryset = []

        if q is not None:
            user_profile = UserProfile.objects.get(
                user__pk=q)
            if device_code is not None:
                queryset = Device.objects.filter(
                    user_profile=user_profile).exclude(device_code=device_code).order_by('device_name')
            else:
                queryset = Device.objects.filter(
                    user_profile=user_profile).order_by('device_name')

        return queryset


class DeviceListApps(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeviceAppSerializer
    queryset = DeviceApp.objects.all().order_by('app_name')

    def post(self, request, *args, **kwargs):
        data = request.data

        serializer = DeviceAppSerializer(data=data['apps'], many=True)
        if serializer.is_valid():
            for app in data['apps']:
                app_name = app['app_name']
                package_name = app['package_name']
                is_block = app['is_block']
                device = get_object_or_404(Device, pk=app['device_id'])
                check_device = DeviceApp.objects.filter(
                    package_name=package_name, device__pk=app['device_id']).exists()

                if not check_device:
                    DeviceApp.objects.create(device=device, app_name=app_name,
                                             package_name=package_name, is_block=is_block)
            return response.Response(data, status=status.HTTP_200_OK)

        return response.Response('error_message: "something went wrong"', status=status.HTTP_400_BAD_REQUEST)


class UpdateDeviceApp(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeviceAppSerializer
    queryset = DeviceApp.objects.all().order_by('app_name')
