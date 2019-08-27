from django.db import models
from django.contrib.auth.models import User

class Vehicle(models.Model):
    plate = models.CharField(max_length=255)
    v_type = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    guard = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.plate
