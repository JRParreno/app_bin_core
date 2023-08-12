from rest_framework import serializers
from .models import AppWeek


class AppWeekSerializer(serializers.ModelSerializer):

    class Meta:
        model = AppWeek
        fields = ['pk', 'start_date', 'end_date',]
