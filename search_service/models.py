from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Favourites(models.Model):
    photo_original_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LocationTag(models.Model):
    location_name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=4, validators=[
                                   MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.DecimalField(max_digits=9, decimal_places=4, validators=[
                                    MinValueValidator(-180), MaxValueValidator(180)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
