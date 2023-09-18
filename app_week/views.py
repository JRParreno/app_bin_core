from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets, permissions, generics, response

from api.paginate import ExtraSmallResultsSetPagination
from device.models import Device
from .serializers import AppWeekSerializer, AppDataSerializer
from .models import AppWeek, AppData
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

        queryset = AppWeek.objects.all().order_by('-date_created')
        if start_date and end_date:
            start_date_object = datetime.strptime(
                start_date, '%m-%d-%Y').date()
            # end_date_object = datetime.strptime(end_date, '%m-%d-%Y').date()
            queryset = AppWeek.objects.filter(
                device__user_profile__user__pk=self.request.user.pk,
                device__device_code=device_code,
                start_date__date=start_date_object).order_by('date_updated')

        return queryset

    def post(self, request, *args, **kwargs):
        device_code = request.data.get('device_code')
        start_date = self.request.data.get('start_date', None)
        end_date = self.request.data.get('end_date', None)

        start_date_object = datetime.strptime(
            start_date, '%m-%d-%Y').date()
        end_date_object = datetime.strptime(end_date, '%m-%d-%Y').date()

        check_appweek_exists = AppWeek.objects.filter(
            device__user_profile__user__pk=self.request.user.pk,
            device__device_code=device_code, start_date__date=start_date_object,
        ).exists()

        user_profile = UserProfile.objects.get(user__pk=self.request.user.pk)

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
            device=check_devices.first(), start_date=start_date_object, end_date=end_date_object,)
        data = {
            "success": "Added appweek"
        }
        return response.Response(data, status=status.HTTP_200_OK)


class AppDataListAddView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppDataSerializer
    queryset = AppData.objects.all().order_by('-date_created')
    pagination_class = ExtraSmallResultsSetPagination

    def get_queryset(self):
        service_pk = self.request.query_params.get('service_pk', None)
        queryset = AppData.objects.all(
            app_service__pk=service_pk).order_by('-date_created')

        return queryset

    def post(self, request, *args, **kwargs):
        package_name = request.data.get('package_name')
        app_name = request.data.get('app_name')
        start_date = self.request.data.get('start_date', None)
        end_date = self.request.data.get('end_date', None)
        service_pk = request.data.get('service_pk')
        hours = request.data.get('hours')
        minutes = request.data.get('minutes')

        start_date_object = datetime.strptime(
            start_date, '%m-%d-%Y').date()
        end_date_object = datetime.strptime(end_date, '%m-%d-%Y').date()

        app_week = AppWeek.objects.get(
            pk=service_pk,    device__user_profile__user__pk=self.request.user.pk
        )

        check_app_datas = AppData.objects.filter(
            app_service=app_week,
            package_name=package_name,
            start_date__date=start_date_object,
        )

        if check_app_datas.exists():
            app_data = check_app_datas.first()

            app_data.hours = hours
            app_data.minutes = minutes
            app_data.save()

            data = {
                "success_message": f"Updated app data {app_data.app_name}"
            }
            return response.Response(data, status=status.HTTP_200_OK)

        new_app_data = AppData.objects.create(app_service=app_week,
                                              app_name=app_name, package_name=package_name,
                                              hours=hours, minutes=minutes, start_date=start_date_object,
                                              end_date=end_date_object
                                              )
        new_app_data.save()

        data = {
            "success_message": f"Added app data {new_app_data.app_name}"
        }
        return response.Response(data, status=status.HTTP_200_OK)
