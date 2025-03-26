from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Booking, Place
from cabregister.models import Cab
from usermanagement.models import User
from .serializers import BookingSerializer

class BookRide(APIView):
    def post(self, request):
        if Booking.objects.filter(user=request.user,completed=False ).exists():
            return Response({"error": "You already have an ongoing booking."}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        # user_id = data.get("user_id")
        driver_id = data.get("driver_id")
        cab_id = data.get("cab_id")
        start_location_data = data.get("start_location")
        end_location_data = data.get("end_location")
        print(driver_id , cab_id , start_location_data , end_location_data)

        if not all([driver_id, cab_id, start_location_data, end_location_data]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, id=request.user.id)
        driver = get_object_or_404(User, id=driver_id)
        cab = get_object_or_404(Cab, id=cab_id)
        cab.busy = True
        cab.save()

        start_location, _ = Place.objects.get_or_create(**start_location_data)
        end_location, _ = Place.objects.get_or_create(**end_location_data)

        booking = Booking.objects.create(
            user=user,
            driver=driver,
            cab=cab,
            start_location=start_location,
            end_location=end_location
        )

        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GetBookingCab(APIView):
    def get(self, request):
        user = request.user

        booking = (
            Booking.objects.select_related("cab", "driver")
            .filter(driver=user, completed=False)
            .order_by("-start_time") 
            .first()
        )

        if not booking:
            return Response({"detail": "No active booking found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)



class CompleteRide(APIView):
    def post(self, request):
        user = request.user

        booking = (
            Booking.objects.select_related("cab", "driver")
            .filter(driver=user, completed=False)
            .order_by("-start_time") 
            .first()
        )

        if not booking:
            return Response({"detail": "No active booking found."}, status=status.HTTP_404_NOT_FOUND)

        booking.completed = True
        booking.save()

        cab = booking.cab
        cab.busy = False
        cab.save()

        return Response({"detail": "Ride completed successfully."}, status=status.HTTP_200_OK)
    


class MyBooking(APIView):
    def get(self, request):
        user = request.user

        booking = (
            Booking.objects.select_related("cab", "driver")
            .filter(user=user, completed=False)
            .order_by("-start_time") 
            .first()
        )

        if not booking:
            return Response({"detail": "No active booking found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingSerializer(booking)
        return Response(serializer.data, status=status.HTTP_200_OK)