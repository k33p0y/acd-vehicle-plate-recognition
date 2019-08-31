from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Vehicle(models.Model):
    plate = models.CharField(max_length=255)
    v_type = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    guard = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.plate

class System(models.Model):
    name = models.CharField(max_length=255)
    value = models.TextField()
    
    def __str__(self):
        return self.name

class Log(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    guard = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_in = models.DateTimeField(default=timezone.now)
    datetime_out = models.DateTimeField(default=None, null=True)
    reason = models.TextField(default='')
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.vehicle.plate
