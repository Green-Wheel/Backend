from django.db import models


# Create your models here.
class TypeVehicle(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "TypeVehicle"
        verbose_name_plural = "TypeVehicles"

    def __str__(self):
        return self.name


class TypeCurrent(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "TypeCurrent"
        verbose_name_plural = "TypeCurrents"

    def __str__(self):
        return self.name


class ChargersType(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    type_vehicle = models.ForeignKey(TypeVehicle, on_delete=models.CASCADE, null=False, blank=False)
    current = models.ForeignKey(TypeCurrent, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "ChargerType"
        verbose_name_plural = "ChargersType"

    def __str__(self):
        return self.id


class Province(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "Province"
        verbose_name_plural = "Provinces"

    def __str__(self):
        return self.id


class Town(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Town"
        verbose_name_plural = "Towns"

    def __str__(self):
        return self.id


class Localizations(models.Model):
    latitude = models.FloatField(null=False, blank=False)
    longitude = models.FloatField(null=False, blank=False)
    direction = models.CharField(max_length=100, null=False, blank=False)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Localization"
        verbose_name_plural = "Localizations"
        unique_together = ["latitude", "longitude"]


class Publication(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(null=False, blank=False)
    latitude = models.ForeignKey(Localizations, on_delete=models.CASCADE, null=False, blank=False, related_name='+')
    longitude = models.ForeignKey(Localizations, on_delete=models.CASCADE, null=False, blank=False, related_name='+')

    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"

    def __str__(self):
        return self.id


class TypeSpeed(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "TypeSpeed"
        verbose_name_plural = "TypeSpeeds"

    def __str__(self):
        return self.name


class Chargers(Publication):
    power = models.FloatField(null=False, blank=False)
    available = models.BooleanField(null=False, blank=False, default=True)
    speed = models.ForeignKey(TypeSpeed, on_delete=models.CASCADE, null=False, blank=False)
    charger_type = models.ForeignKey(ChargersType, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Charger"
        verbose_name_plural = "Chargers"


class PublicChargers(Chargers):
    agent = models.CharField(max_length=50, null=False, blank=False)
    identifier = models.CharField(max_length=50, null=False, blank=False)
    access = models.CharField(max_length=50, null=False, blank=False)


# class PrivateChargers(Chargers):