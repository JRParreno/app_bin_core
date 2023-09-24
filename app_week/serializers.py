from rest_framework import serializers
from .models import AppData


class AppDataSerializer(serializers.ModelSerializer):
    device_code = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = AppData
        fields = ['pk', 'app_name', 'package_name',
                  'hours', 'minutes', 'start_date', 'end_date',
                  'date_created', 'date_updated', 'device', 'device_code'
                  ]
        extra_kwargs = {
            'device': {'read_only': True},
        }
