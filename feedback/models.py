from django.db import models
from cabregister.models import Cab
from django.core.validators import MinValueValidator , MaxValueValidator
from usermanagement.models import User
# Create your models here.


class Review(models.Model):
    cab = models.ForeignKey(Cab, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Review by {self.user} on {self.cab}"
