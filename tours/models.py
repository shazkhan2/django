from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Tours(models.Model):   
    assigned_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_tours'
    )

    driver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tours'
    )

    passenger_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    pickup_time = models.DateTimeField()
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    dropoff_time = models.DateTimeField()


    def __str__(self):
        return self.passenger_name