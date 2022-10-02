from django.db import models

from api.users.models import Users
# from api.chargers.models import ChargersType
from config import settings


# Create your models here.
class CarsBrand(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "CarBrand"
        verbose_name_plural = "CarsBrand"

    def __str__(self):
        return self.name


class CarsModel(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    year = models.DateField(null=True, blank=True)
    autonomy = models.FloatField(null=True, blank=True)
    car_brand = models.ForeignKey(CarsBrand, on_delete=models.CASCADE, null=False, blank=False)

    # charger_type = models.ManyToManyField(ChargersType)

    class Meta:
        verbose_name = "CarModel"
        verbose_name_plural = "CarsModel"
        unique_together = ["car_brand", "name", "year"]

    def __str__(self):
        return self.name


class Cars(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    charge_capacity = models.FloatField(null=False, blank=False, default=-1)
    car_license = models.CharField(max_length=10, null=False, blank=False)
    model_id = models.ForeignKey(CarsModel, on_delete=models.CASCADE, null=False, blank=False)
    car_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"

    def __str__(self):
        return self.name
