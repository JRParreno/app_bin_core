from rest_framework import serializers
from .models import AppWeek


class AppWeekSerializer(serializers.ModelSerializer):
    device_code = serializers.CharField(write_only=True)

    class Meta:
        model = AppWeek
        fields = ['pk', 'start_date', 'end_date', 'device_code',]
