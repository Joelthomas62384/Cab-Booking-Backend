from rest_framework import serializers
from . models import Cab
from usermanagement.serializers import UserSerializer


    
class CabSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    estimated_price = serializers.SerializerMethodField()

    class Meta:
        model = Cab
        fields = (
            'id', 'car_number', 'driver_age', 'driving_license', 'languages',
            'car_details', 'mobile_number', 'vehicle_rc', 'vehicle_type',
            'price_per_km', 'approved', 'driver_image', 'on_dutty', 'busy',
            'user', 'estimated_price'
        )
        read_only_fields = ('id', 'user', 'approved', 'busy')

    def get_estimated_price(self, obj):
        estimated_distance = self.context.get("estimated_distance")  # Distance in KM
        BASE_FARE = 50  # Fixed base charge
        FUEL_COST_PER_KM = 5  # Fuel cost per KM
        MAINTENANCE_COST_PER_KM = 2  # Maintenance per KM
        DRIVER_PROFIT_MARGIN = 1.05  # 5% profit margin for long trips
        LONG_DISTANCE_DISCOUNT = 0.5  # 50% discount for trips above 150 km

        if estimated_distance is not None and estimated_distance > 0:
            # Dynamic pricing per km
            if estimated_distance > 150:
                price_per_km = obj.price_per_km * LONG_DISTANCE_DISCOUNT  # 50% discount
            elif estimated_distance > 100:
                price_per_km = obj.price_per_km * 0.65  # 35% discount
            elif estimated_distance > 50:
                price_per_km = obj.price_per_km * 0.80  # 20% discount
            else:
                price_per_km = obj.price_per_km  # No discount

            # Cost calculations
            fuel_cost = FUEL_COST_PER_KM * estimated_distance
            maintenance_cost = MAINTENANCE_COST_PER_KM * estimated_distance
            ride_fare = price_per_km * estimated_distance

            # Apply base fare and driver profit margin
            estimated_price = ((BASE_FARE + fuel_cost + maintenance_cost + ride_fare) * DRIVER_PROFIT_MARGIN)/2

            if estimated_distance < 50:
                estimated_price +=300
            

            return round(estimated_price, 2)

        return None  

