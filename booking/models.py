from django.db import models
from cabregister.models import Cab
from usermanagement.models import User

class Place(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=None, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=None, blank=True, null=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    start_location = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="start_bookings")
    end_location = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="end_bookings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bookings")
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="driver_bookings")
    cab = models.ForeignKey(Cab, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking from {self.start_location} to {self.end_location}"
