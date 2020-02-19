from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Vehicle(models.Model):
    plate = models.CharField(max_length=255)
    v_type = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    guard = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(default=timezone.now, null=True)
    first_entry_at = models.DateTimeField(default=timezone.now, null=True)
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
    edited_by = models.ForeignKey(User, related_name='edited_by', on_delete=models.CASCADE, default=None, null=True)
    edited_at = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return self.vehicle.plate

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    username = forms.CharField(max_length=30, required=False, help_text='Optional.')
    password = forms.CharField(max_length=30, required=False, help_text='Optional.')
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')