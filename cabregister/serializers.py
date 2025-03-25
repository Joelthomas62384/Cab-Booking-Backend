from rest_framework import serializers
from . models import Cab


    


class CabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cab
        fields = (
            'id', 'car_number', 'driver_age', 'driving_license', 'languages',
            'car_details', 'mobile_number', 'vehicle_rc', 'vehicle_type',
            'price_per_km', 'approved', 'driver_image', 'on_dutty', 'busy'
        )
        read_only_fields = ('id', 'user', 'approved','busy')
        extra_kwargs = {
            'driver_image': {'required': True},
            'vehicle_type': {'required': True},
            'price_per_km': {'required': True, 'min_value': 1}
        }
