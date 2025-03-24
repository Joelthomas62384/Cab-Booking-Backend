from rest_framework import serializers
from . models import CabImages,Cab

class CabImagesSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = CabImages
        fields = ('image','cab')

    def get_image(self, obj):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(obj.image.url)
        return None

    


class CabSerializer(serializers.ModelSerializer):
    cab_images = CabImagesSerializer(many=True, read_only=True)
    class Meta:
        model = Cab
        fields = ('id',  'car_number', 'adhar', 'driving_license', 'vehicle_rc', 'vehicle_type', 'price_per_km', 'approved',  'busy', 'cab_images' ,'driver_image')
        read_only = (
            'id','user' , 'approved'
        )
        extra_kwargs = {
            'driver_image' : {'required': True}
        }

        