from django import forms
from django.db import models
from config import settings

# Create your models here.
class Province(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "Province"
        verbose_name_plural = "Provinces"

    def __str__(self):
        return self.name


class Town(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
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
    title = models.CharField(max_length=50, null=True, blank=False)
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

class OccupationRangesType(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "OccupationRangesType"
        verbose_name_plural = "OccupationRangesTypes"

    def __str__(self):
        return self.name


class OccupationRanges(models.Model):
    start_date = models.DateTimeField(null=True, blank=False)
    end_date = models.DateTimeField(null=True, blank=False)
    occupation_range_type = models.ForeignKey(OccupationRangesType, on_delete=models.CASCADE, null=True, blank=False)
    related_publication = models.ForeignKey(Publication, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "OccupationRange"
        verbose_name_plural = "OccupationRanges"
        unique_together = ["start_date", "end_date", "related_publication"]

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        if end_date < start_date:
            raise forms.ValidationError("End date should be greater than start date.", code='EndGreaterThanStart')

        start_occupations = OccupationRanges.objects.filter(start_date__gte=start_date, start_date__lte=end_date)
        end_occupations = OccupationRanges.objects.filter(end_date__gte=start_date, end_date__lte=end_date)
        if start_occupations or end_occupations:
            raise forms.ValidationError("Occupation range already exists.", code="AlreadyExists")

    def __str__(self):
        return str(self.id)
