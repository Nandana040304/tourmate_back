from django.db import models

class Place(models.Model):
    CATEGORY_CHOICES = [
        ('Tourist Places', 'Tourist Places'),
        ('Hospitals', 'Hospitals'),
        ('Police Stations', 'Police Stations'),
        ('Restaurants', 'Restaurants'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='places/')
    description = models.TextField()

    def __str__(self):
        return self.name