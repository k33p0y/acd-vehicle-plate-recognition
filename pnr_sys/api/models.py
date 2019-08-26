from django.db import models

class Latest(models.Model):
    plate = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.plate