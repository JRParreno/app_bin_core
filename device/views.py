from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets, permissions, generics, response

from api.paginate import ExtraSmallResultsSetPagination
from .serializers import DeviceSerializer
from .models import Device
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

            Device.objects.create(
                user_profile=user_profile,
                device_code=device_code,
                device_name=device_name,
            )

            data = {
                "succecss": "Device added successfully"
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
        queryset = Device.objects.all().order_by('device_name')
        if q:
            queryset = Device.objects.filter(
                device_code=q).order_by('device_name')

        return queryset
