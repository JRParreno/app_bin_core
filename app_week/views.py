from django.shortcuts import get_object_or_404, render
from rest_framework import status, viewsets, permissions, generics, response

from api.paginate import ExtraSmallResultsSetPagination
from .serializers import AppWeekSerializer
from .models import AppWeek
from user_profile.models import UserProfile


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

    # def post(self, request, *args, **kwargs):
    #     device_code = request.data.get('device_code')

    #     check_device_exists = Device.objects.filter(device_code=device_code).exists
    #     if check_device_exists:
    #         error = {
    #             "error_message": "Device Already Exists"
    #         }
    #         return response.Response(error, status=status.HTTP_200_OK)
    #     return super().post(request, *args, **kwargs)
