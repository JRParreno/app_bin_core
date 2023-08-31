from rest_framework import serializers
from .models import AppWeek, AppData


class AppWeekSerializer(serializers.ModelSerializer):
    device_code = serializers.CharField(write_only=True)

    class Meta:
        model = AppWeek
        fields = ['pk', 'start_date', 'end_date', 'device_code',]


class AppDataSerializer(serializers.ModelSerializer):
    service_pk = serializers.CharField(write_only=True)

    class Meta:
        model = AppData
        fields = ['pk', 'app_service', 'appName', 'packageName',
                  'hours', 'minutes', 'start_date', 'end_date',
                  'date_created', 'date_update', 'service_pk'
                  ]
