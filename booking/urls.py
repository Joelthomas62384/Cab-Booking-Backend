from django.urls import path
from .views import *
urlpatterns = [
    path("book" ,BookRide.as_view() ),
    path("get-booking-cab" , GetBookingCab.as_view() ),
    path('complete-ride' , CompleteRide.as_view() ),
    path('my-booking', MyBooking.as_view())
]
