from django.contrib.auth.models import User
from api.bookings.models import Bookings
from django.db import models
from django.template.backends import django

from api.chargers.models import Publication


class Report(models.Model):
    message = models.TextField(null=False, blank=False)
    image = models.TextField(null=True, blank=True)
    data_reported = models.DateTimeField(default=django.utils.timezone.now, verbose_name='data reported')

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        abstract = True

    def __str__(self):
        return self.id


class TypeResolution(models.Model):
    type = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "Type Resolution"
        verbose_name_plural = "Type Resolutions"

    def __str__(self):
        return self.type


class Moderator(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Moderator"
        verbose_name_plural = "Moderators"

    def __str__(self):
        return self.id


class FeedbackReport(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    id_report = models.ForeignKey(Report, on_delete=models.CASCADE, null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    resolution = models.ForeignKey(TypeResolution, on_delete=models.CASCADE, null=False, blank=False)
    data_resolution = models.DateTimeField(default=django.utils.timezone.now, verbose_name='data resolution')

    class Meta:
        verbose_name = "Feedback Report"
        verbose_name_plural = "Feedback Reports"

    def __str__(self):
        return self.id


class SectionReportValoration(models.Model):
    id_report = models.ForeignKey(Report, on_delete=models.CASCADE, null=False, blank=False)
    id_reserva = models.ForeignKey(Bookings, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Section Report Valoration"
        verbose_name_plural = "Section Report Valorations"

    def __str__(self):
        return self.id


class SectionReportPublication(models.Model):
    id_report = models.ForeignKey(Report, on_delete=models.CASCADE, null=False, blank=False)
    id_publication = models.ForeignKey(Publication, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Section Report Publication"
        verbose_name_plural = "Section Report Publications"

    def __str__(self):
        return self.id


class SectionReportUser(models.Model):
    id_report = models.ForeignKey(Report, on_delete=models.CASCADE, null=False, blank=False)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    username = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Section Report User"
        verbose_name_plural = "Section Report Users"

    def __str__(self):
        return self.id
