from django.db import models

class PoliceStation(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()   # 👈 ADD THIS

    def __str__(self):
        return self.name