from django.db import models

from api.chargers.models import Publication


# Create your models here.

class BikeTypes(models.Model):
    name = models.CharField(max_length=50, null=True, blank=False, unique=True)

    class Meta:
        verbose_name = "BikeType"
        verbose_name_plural = "BikeTypes"

    def __str__(self):
        return self.name


class Bikes(Publication):
    bike_type = models.ForeignKey(BikeTypes, on_delete=models.CASCADE, null=False, blank=False)
    power = models.FloatField(null=True, blank=False)
    price = models.FloatField(null=True, blank=False)

    class Meta:
        verbose_name = "Bike"
        verbose_name_plural = "Bikes"

    def __str__(self):
        return str(self.title)
