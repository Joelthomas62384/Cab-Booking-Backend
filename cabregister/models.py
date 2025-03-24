from django.db import models
from django.contrib.auth import get_user_model


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
    adhar = models.ImageField(upload_to='adhar car owner')
    driving_license = models.ImageField(upload_to='driving license')
    vehicle_rc = models.ImageField(upload_to='Vehicle')
    vehicle_type = models.CharField(max_length=150)
    price_per_km = models.PositiveIntegerField()
    approved = models.BooleanField(default=False)
    driver_image = models.ImageField(upload_to='driver image' , null=True , blank=True)
    on_dutty= models.BooleanField(default=False)
    busy = models.BooleanField(default=False)


    def __str__(self):
        return self.user.full_name + " - " + self.vehicle_type + f"({self.car_number})"



class CabImages(models.Model):
    cab = models.ForeignKey(Cab, related_name="cab_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='cab_images', null=True , blank=True)



class CabLocationHistory(models.Model):
    cab = models.ForeignKey("Cab", on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)