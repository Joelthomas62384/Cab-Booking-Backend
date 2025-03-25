from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator , MaxValueValidator


User = get_user_model()



class Cab(models.Model):
    vehicle_type_choices = (
        (
            ('1' , 'Car'),
            ('2' , 'Auto')
        )
    )
    user = models.OneToOneField(User, related_name="cab_owner",on_delete=models.CASCADE)
    car_number = models.CharField(max_length=150)
    driver_age = models.PositiveIntegerField(default=19 , validators=[
        MinValueValidator(18) 
    ])
    driving_license = models.ImageField(upload_to='driving license')
    languages = models.TextField(null=True ,blank=True)
    car_details = models.JSONField(null=True , blank=True)
    mobile_number = models.CharField(max_length=15,null=True , blank= True)
    vehicle_rc = models.ImageField(upload_to='Vehicle')
    vehicle_type = models.CharField(choices=vehicle_type_choices,max_length=150)
    price_per_km = models.PositiveIntegerField()
    approved = models.BooleanField(default=False)
    driver_image = models.ImageField(upload_to='driver image' , null=True , blank=True)
    on_dutty= models.BooleanField(default=False)
    busy = models.BooleanField(default=False)


    def __str__(self):
        return self.user.full_name + " - " + self.vehicle_type + f"({self.car_number})"






class CabLocationHistory(models.Model):
    cab = models.ForeignKey("Cab", on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)