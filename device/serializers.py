from rest_framework import serializers
from .models import Device

class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ['pk',
                  'device_name', 
                  'device_code',
                  ]

    
    def __init__(self, *args, **kwargs):
        # init context and request
        context = kwargs.get('context', {})
        self.request = context.get('request', None)
        self.kwargs = context.get("kwargs", None)

        super(DeviceSerializer, self).__init__(*args, **kwargs)


    def create(self, validated_data):
        current_user = self.request.user

        user_profile = current_user.profile
        device_name = validated_data.pop('device_name')
        device_code = validated_data.pop('device_code')

        instance = Device.objects.create(user_profile=user_profile, device_name=device_name, device_code=device_code)

        
        return instance
