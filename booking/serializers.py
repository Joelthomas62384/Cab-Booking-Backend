from rest_framework import serializers
from .models import Place, Booking
# from django.contrib.auth.models import User  
# from .models import Cab 

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'name', 'latitude', 'longitude']


class BookingSerializer(serializers.ModelSerializer):
    start_location = PlaceSerializer()
    end_location = PlaceSerializer()
    user = serializers.StringRelatedField()  
    driver = serializers.StringRelatedField()
    cab = serializers.StringRelatedField()

    class Meta:
        model = Booking
        fields = ['id', 'start_location', 'end_location', 'user', 'driver', 'cab', 'start_time', 'end_time', 'completed']

    def create(self, validated_data):
        start_location_data = validated_data.pop('start_location')
        end_location_data = validated_data.pop('end_location')
        start_location = Place.objects.create(**start_location_data)
        end_location = Place.objects.create(**end_location_data)
        
        return Booking.objects.create(start_location=start_location, end_location=end_location, **validated_data)

    def update(self, instance, validated_data):
        if 'start_location' in validated_data:
            start_location_data = validated_data.pop('start_location')
            instance.start_location.name = start_location_data.get('name', instance.start_location.name)
            instance.start_location.latitude = start_location_data.get('latitude', instance.start_location.latitude)
            instance.start_location.longitude = start_location_data.get('longitude', instance.start_location.longitude)
            instance.start_location.save()

        if 'end_location' in validated_data:
            end_location_data = validated_data.pop('end_location')
            instance.end_location.name = end_location_data.get('name', instance.end_location.name)
            instance.end_location.latitude = end_location_data.get('latitude', instance.end_location.latitude)
            instance.end_location.longitude = end_location_data.get('longitude', instance.end_location.longitude)
            instance.end_location.save()
        
        return super().update(instance, validated_data)
