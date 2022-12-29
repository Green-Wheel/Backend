from django.db import models

from api.publications.models import Publication


# Create your models here.
class CurrentsType(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "CurrentsType"
        verbose_name_plural = "CurrentsTypes"

    def __str__(self):
        return self.name


class ConnectionsType(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    current_type = models.ForeignKey(CurrentsType, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "ConnectionsType"
        verbose_name_plural = "ConnectionsTypes"

    def __str__(self):
        return self.name


class SpeedsType(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "SpeedsType"
        verbose_name_plural = "SpeedsTypes"

    def __str__(self):
        return self.name


class Chargers(Publication):
    power = models.FloatField(null=True, blank=False)
    speed = models.ManyToManyField(SpeedsType)
    connection_type = models.ManyToManyField(ConnectionsType)
    current_type = models.ManyToManyField(CurrentsType)

    class Meta:
        verbose_name = "Charger"
        verbose_name_plural = "Chargers"

    def __str__(self):
        return str(self.id)


class PublicChargers(Chargers):
    agent = models.TextField(null=True, blank=False)
    identifier = models.CharField(max_length=100, null=True, blank=False)
    access = models.CharField(max_length=100, null=True, blank=False)

    class Meta:
        verbose_name = "PublicCharger"
        verbose_name_plural = "PublicChargers"

    def __str__(self):
        return self.title


class PrivateChargers(Chargers):
    price = models.FloatField(null=True, blank=False)

    class Meta:
        verbose_name = "PrivateCharger"
        verbose_name_plural = "PrivateChargers"

    def __str__(self):
        return str(self.price)


class Configs(models.Model):
    key = models.CharField(max_length=50, null=False, blank=False, unique=True)
    value = models.CharField(max_length=150, null=False, blank=False)

    class Meta:
        verbose_name = "Config"
        verbose_name_plural = "Configs"

    def __str__(self):
        return str(self.id)
