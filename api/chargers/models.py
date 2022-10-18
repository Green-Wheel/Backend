from django.db import models


# Create your models here.
class CurrentsType(models.Model):
    name = models.CharField(max_length=50, null=True, blank=False, unique=True)

    class Meta:
        verbose_name = "CurrentsType"
        verbose_name_plural = "CurrentsTypes"

    def __str__(self):
        return self.name


class ConnectionsType(models.Model):
    name = models.CharField(max_length=50, null=True, blank=False, unique=True)

    class Meta:
        verbose_name = "ConnectionsType"
        verbose_name_plural = "ConnectionsTypes"

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=50, null=True, blank=False, unique=True)

    class Meta:
        verbose_name = "Province"
        verbose_name_plural = "Provinces"

    def __str__(self):
        return self.name


class Town(models.Model):
    name = models.CharField(max_length=50, null=True, blank=False, unique=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Town"
        verbose_name_plural = "Towns"

    def __str__(self):
        return self.name


class Localizations(models.Model):
    latitude = models.FloatField(null=True, blank=False)
    longitude = models.FloatField(null=True, blank=False)
    direction = models.CharField(max_length=100, null=True, blank=False)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, null=True, blank=False)

    class Meta:
        verbose_name = "Localization"
        verbose_name_plural = "Localizations"
        unique_together = ["latitude", "longitude"]

    def __str__(self):
        return self.latitude, self.longitude


class Publication(models.Model):
    title = models.CharField(max_length=50, null=True, blank=False)
    description = models.TextField(null=True, blank=True)
    localization = models.ForeignKey(Localizations, on_delete=models.CASCADE, null=True, blank=False, related_name='+')

    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"

    def __str__(self):
        return self.title


class SpeedsType(models.Model):
    name = models.CharField(max_length=50, null=True, blank=False, unique=True)

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
    available = models.BooleanField(null=True, blank=False, default=True)

    class Meta:
        verbose_name = "Charger"
        verbose_name_plural = "Chargers"

    def __str__(self):
        return self.id


class PublicChargers(Chargers):
    agent = models.CharField(max_length=50, null=True, blank=False)
    identifier = models.CharField(max_length=50, null=True, blank=False)
    access = models.CharField(max_length=50, null=True, blank=False)

    def __str__(self):
        return self.id


class PrivateChargers(Chargers):
    price = models.FloatField(null=True, blank=False)

    def __str__(self):
        return self.id
