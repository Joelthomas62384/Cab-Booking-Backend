from rest_framework.views import APIView
from . serializers import *
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.shortcuts import get_object_or_404
import json
import redis
from geopy.distance import geodesic    

class CabView(APIView):

    def get(self, request):
        approved_str = request.query_params.get('approved', 'false').lower()
        approved = approved_str in ['true', '1', 'yes']  
        
        cabs = Cab.objects.filter(approved=approved, busy=False)
        
        serializer = CabSerializer(cabs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        user = request.user
        if Cab.objects.filter(user=user).exists():
            return Response({'message' : "This account has a driver account already"}  , status=status.HTTP_400_BAD_REQUEST)

        data = request.data

        serializer = CabSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class ApproveView(APIView):
    def put(self, request, pk):
        cab = get_object_or_404(Cab, pk=pk)
        cab.approved = not cab.approved
        cab.save()
        return Response({'message' : "Cab approved successfully"}  , status=status.HTTP_200_OK)
    
redis_client = redis.StrictRedis(host="redis", port=6379, db=0, decode_responses=True)

class GetFreeCabs(APIView):
    
    BASE_FARE = 50  # Base fare in currency units
    RATE_PER_KM = 10  # Rate per km in currency units

    def post(self, request):
        from_location = request.data.get("from")
        to_location = request.data.get("to")

        if not from_location:
            return Response({"error": "Start location is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not to_location:
            return Response({"error": "Destination location is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            start_lat = float(from_location.get("latitude"))
            start_lng = float(from_location.get("longitude"))
            end_lat = float(to_location.get("latitude"))
            end_lng = float(to_location.get("longitude"))
        except (TypeError, ValueError):
            return Response({"error": "Invalid latitude or longitude"}, status=status.HTTP_400_BAD_REQUEST)

        print("📍 Searching for cabs near:", start_lat, start_lng)

        start_coords = (start_lat, start_lng)
        end_coords = (end_lat, end_lng)

        # Calculate trip distance
        trip_distance = geodesic(start_coords, end_coords).km  

        # Estimate price
        estimated_price = self.BASE_FARE + (trip_distance * self.RATE_PER_KM)

        available_cabs = Cab.objects.filter(busy=False,approved=True)

        nearby_cabs = []
        for cab in available_cabs:
            cab_coords = (cab.latitude, cab.longitude)
            distance = geodesic(start_coords, cab_coords).km 
            if distance <= 5:  
                cab.distance = distance
                nearby_cabs.append(cab)

        if not nearby_cabs:
            return Response({"message": "No cabs available nearby"}, status=status.HTTP_200_OK)

        # Sort by nearest cabs and limit to 50
        nearby_cabs = sorted(nearby_cabs, key=lambda x: x.distance)[:50]

        serializer = CabSerializer(nearby_cabs, many=True, context={"request": request})

        return Response(
            {
                "cabs": serializer.data,
                "trip_distance_km": round(trip_distance, 2),
                "estimated_price": round(estimated_price, 2),
            },
            status=status.HTTP_200_OK
        )

class UpdatePath(APIView):
  
    def post(self, request):
        user = request.user  # Ensure authentication is enabled
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")

        if not latitude or not longitude:
            return Response({"error": "Latitude and longitude are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            rider = Cab.objects.get(user=user)
            rider.latitude = latitude
            rider.longitude = longitude
            rider.save()

            return Response({"message": "Location updated successfully"}, status=status.HTTP_200_OK)
        except Cab.DoesNotExist:
            return Response({"error": "Rider not found"}, status=status.HTTP_404_NOT_FOUND)
