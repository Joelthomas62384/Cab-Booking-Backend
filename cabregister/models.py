from django.db import models
from django.core.validators import MinValueValidator

class Cab(models.Model):
    VEHICLE_TYPE_CHOICES = (
        ('1', 'Car'),
        ('2', 'Auto'),
    )

    user = models.OneToOneField("usermanagement.User", related_name="cab_owner", on_delete=models.CASCADE)
    car_number = models.CharField(max_length=150)
    driver_age = models.PositiveIntegerField(default=19, validators=[
        MinValueValidator(18) 
    ])
    driving_license = models.ImageField(upload_to='driving_license')
    languages = models.TextField(null=True, blank=True)
    car_details = models.JSONField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    vehicle_rc = models.ImageField(upload_to='vehicle')
    vehicle_type = models.CharField(choices=VEHICLE_TYPE_CHOICES, max_length=150)
    price_per_km = models.PositiveIntegerField(default=40)
    approved = models.BooleanField(default=False)
    driver_image = models.ImageField(upload_to='driver_image', null=True, blank=True)
    on_dutty = models.BooleanField(default=False)
    busy = models.BooleanField(default=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=None, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=None, blank=True, null=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.car_number}"
