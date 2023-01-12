from django import forms
from django.db import models

from api.bookings.models import Bookings
from config import settings


# Create your models here.
class Province(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "Province"
        verbose_name_plural = "Provinces"

    def __str__(self):
        return self.name


class Town(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Town"
        verbose_name_plural = "Towns"

    def __str__(self):
        return self.name


class Localizations(models.Model):
    latitude = models.FloatField(null=True, blank=False)
    longitude = models.FloatField(null=True, blank=False)

    class Meta:
        verbose_name = "Localization"
        verbose_name_plural = "Localizations"
        unique_together = ["latitude", "longitude"]

    def __str__(self):
        return self.latitude, self.longitude


class Publication(models.Model):
    title = models.TextField(null=True, blank=False)
    description = models.TextField(null=True, blank=True)
    direction = models.CharField(max_length=100, null=True, blank=False)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, null=True, blank=False)
    localization = models.ForeignKey(Localizations, on_delete=models.CASCADE, null=True, blank=False, related_name='+')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"

    def __str__(self):
        return str(self.id)


class Images(models.Model):
    image_path = models.URLField(null=False, blank=False)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, null=True, blank=False)

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    def __str__(self):
        return str(self.id)


class Contamination(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.DO_NOTHING, null=False, blank=False)
    contamination = models.TextField(null=True, blank=False)
    class Meta:
        verbose_name = "Contamination"
        verbose_name_plural = "Contaminations"


class OccupationRangesType(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "OccupationRangesType"
        verbose_name_plural = "OccupationRangesTypes"

    def __str__(self):
        return self.name


class OccupationRepeatMode(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "RepeatMode"
        verbose_name_plural = "RepeatModes"

    def __str__(self):
        return self.name


class OccupationRanges(models.Model):
    start_date = models.DateTimeField(null=True, blank=False)
    end_date = models.DateTimeField(null=True, blank=False)
    occupation_range_type = models.ForeignKey(OccupationRangesType, on_delete=models.CASCADE, null=False, blank=False,
                                              default=2)
    related_publication = models.ForeignKey(Publication, on_delete=models.CASCADE, null=False, blank=False)
    repeat_mode = models.ForeignKey(OccupationRepeatMode, on_delete=models.CASCADE, null=False, blank=False, default=1)
    booking = models.OneToOneField(Bookings, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "OccupationRange"
        verbose_name_plural = "OccupationRanges"
        unique_together = ["start_date", "end_date", "related_publication"]

    def __str__(self):
        return str(self.id)
