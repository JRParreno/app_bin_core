from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets, permissions, generics, response

from api.paginate import ExtraSmallResultsSetPagination
from device.models import Device
from .serializers import AppWeekSerializer
from .models import AppWeek
from user_profile.models import UserProfile
from datetime import datetime


class AppWeekListAddView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppWeekSerializer
    queryset = AppWeek.objects.all().order_by('date_updated')
    pagination_class = ExtraSmallResultsSetPagination

    def get_queryset(self):
        device_code = self.request.query_params.get('device_code', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        queryset = AppWeek.objects.all().order_by('date_updated')
        if start_date and end_date:
            queryset = AppWeek.objects.filter(device__device_code=device_code,
                                              start_date=start_date, end_date=end_date).order_by('date_updated')

        return queryset

    def post(self, request, *args, **kwargs):
        device_code = request.data.get('device_code')
        start_date_str = request.data.get('start_date')
        end_date_str = request.data.get('end_date')

        start_date = datetime.fromisoformat(start_date_str)

        end_date = datetime.fromisoformat(end_date_str)

        check_appweek_exists = AppWeek.objects.filter(device__device_code=device_code, start_date__date=start_date,
                                                      end_date__date=end_date,
                                                      ).exists()

        user_profile = UserProfile.objects.get(pk=self.request.user.pk)

        check_devices = Device.objects.filter(
            user_profile=user_profile,
            device_code=device_code)

        if not check_devices.exists():
            error = {
                "error_message": "Device not found"
            }
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

        if check_appweek_exists:
            error = {
                "error_message": "Already added app week"
            }
            return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

        AppWeek.objects.create(
            device=check_devices.first(), start_date=start_date, end_date=end_date,)
        data = {
            "success": "Added appweek"
        }
        return response.Response(data, status=status.HTTP_200_OK)
