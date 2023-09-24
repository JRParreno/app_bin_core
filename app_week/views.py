from rest_framework import status, permissions, generics, response
from django.shortcuts import get_object_or_404, render

from api.paginate import ExtraSmallResultsSetPagination
from device.models import Device
from .serializers import AppDataSerializer
from .models import AppData
from user_profile.models import UserProfile
from datetime import datetime


# class AppWeekListAddView(generics.ListCreateAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = AppWeekSerializer
#     queryset = AppWeek.objects.all().order_by('date_updated')
#     pagination_class = ExtraSmallResultsSetPagination

#     def get_queryset(self):
#         device_code = self.request.query_params.get('device_code', None)
#         start_date = self.request.query_params.get('start_date', None)
#         end_date = self.request.query_params.get('end_date', None)

#         queryset = AppWeek.objects.all().order_by('-date_created')
#         if start_date and end_date:
#             start_date_object = datetime.strptime(
#                 start_date, '%m-%d-%Y').date()
#             # end_date_object = datetime.strptime(end_date, '%m-%d-%Y').date()
#             queryset = AppWeek.objects.filter(
#                 device__user_profile__user__pk=self.request.user.pk,
#                 device__device_code=device_code,
#                 start_date__date=start_date_object).order_by('date_updated')

#         return queryset

#     def post(self, request, *args, **kwargs):
#         device_code = request.data.get('device_code')
#         start_date = self.request.data.get('start_date', None)
#         end_date = self.request.data.get('end_date', None)

#         start_date_object = datetime.strptime(
#             start_date, '%m-%d-%Y').date()
#         end_date_object = datetime.strptime(end_date, '%m-%d-%Y').date()

#         check_appweek_exists = AppWeek.objects.filter(
#             device__user_profile__user__pk=self.request.user.pk,
#             device__device_code=device_code, start_date__date=start_date_object,
#         ).exists()

#         user_profile = UserProfile.objects.get(user__pk=self.request.user.pk)

#         check_devices = Device.objects.filter(
#             user_profile=user_profile,
#             device_code=device_code)

#         if not check_devices.exists():
#             error = {
#                 "error_message": "Device not found"
#             }
#             return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

#         if check_appweek_exists:
#             error = {
#                 "error_message": "Already added app week"
#             }
#             return response.Response(error, status=status.HTTP_400_BAD_REQUEST)

#         AppWeek.objects.create(
#             device=check_devices.first(), start_date=start_date_object, end_date=end_date_object,)
#         data = {
#             "success": "Added appweek"
#         }
#         return response.Response(data, status=status.HTTP_200_OK)


class AppDataListAddView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AppDataSerializer
    queryset = AppData.objects.all().order_by('-date_created')
    pagination_class = ExtraSmallResultsSetPagination

    def get_queryset(self):

        device_code = self.request.query_params.get('device_code', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date and end_date:
            # start_date_object = datetime.strptime(
            #     start_date, '%m-%d-%Y').date()
            # end_date_object = datetime.strptime(end_date, '%m-%d-%Y').date()

            queryset = AppData.objects.filter(
                device__user_profile__user__pk=self.request.user.pk,
                device__device_code=device_code,
                start_date__range=[start_date, end_date]).order_by('start_date')

            return queryset

        return []

    def post(self, request, *args, **kwargs):
        package_name = request.data.get('package_name')
        app_name = request.data.get('app_name')
        start_date = self.request.data.get('start_date', None)
        end_date = self.request.data.get('end_date', None)
        device_code = request.data.get('device_code')
        hours = request.data.get('hours')
        minutes = request.data.get('minutes')

        # start_date_object = datetime.strptime(
        #     start_date, '%m-%d-%Y').date()
        # end_date_object = datetime.strptime(end_date, '%m-%d-%Y').date()

        user_profile = UserProfile.objects.get(user__pk=self.request.user.pk)

        device = get_object_or_404(
            Device, device_code=device_code, user_profile=user_profile)

        check_app_datas = AppData.objects.filter(
            device__pk=device.pk,
            package_name=package_name,
            start_date=start_date
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

        new_app_data = AppData.objects.create(device=device,
                                              app_name=app_name, package_name=package_name,
                                              hours=hours, minutes=minutes, start_date=start_date,
                                              end_date=end_date
                                              )
        new_app_data.save()

        data = {
            "success_message": f"Added app data {new_app_data.app_name}"
        }
        return response.Response(data, status=status.HTTP_200_OK)
