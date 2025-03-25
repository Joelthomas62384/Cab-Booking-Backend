from rest_framework import serializers
import re
from . models import User
from cabregister.models import Cab

class LoginSerializer(serializers.Serializer):
    mobile = serializers.CharField(min_length=10, max_length = 15)
    password = serializers.CharField(max_length=150)

    def validate_mobile(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Mobile number must contain only digits.")
        
        if not (10 <= len(value) <= 15):
            raise serializers.ValidationError("Mobile number must be between 10 to 15 digits long.")

        return value


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=150, write_only=True)
    is_driver = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = User
        fields = ( 'mobile', 'full_name', 'password','is_driver')
        # extra_kwargs = {
        #     'password': {'write_only': True, 'required': True},
        # }

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user
    
    def validate_mobile(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Mobile number must contain only digits.")
        
        if not (10 <= len(value) <= 15):
            raise serializers.ValidationError("Mobile number must be between 10 to 15 digits long.")

        return value
    
    def get_is_driver(self, obj):
        return Cab.objects.filter(user=obj , approved=True).exists()

