
from api.bookings.models import Bookings
from django.db import models
from api.chargers.models import Publication
from django.conf import settings


class Report(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    image = models.TextField(null=True, blank=True)
    data_reported = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        # abstract = True

    def __str__(self):
        return self.id


class TypeResolution(models.Model):
    type = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "Type Resolution"
        verbose_name_plural = "Type Resolutions"

    def __str__(self):
        return self.type


class FeedbackReport(models.Model):
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, related_name="moderator")
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    resolution = models.ForeignKey(TypeResolution, on_delete=models.CASCADE, null=False, blank=False)
    data_resolution = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Feedback Report"
        verbose_name_plural = "Feedback Reports"

    def __str__(self):
        return self.id


class SectionReportValoration(Report):
    reserva = models.ForeignKey(Bookings, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Section Report Valoration"
        verbose_name_plural = "Section Report Valorations"

    def __str__(self):
        return self.id


class SectionReportPublication(Report):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Section Report Publication"
        verbose_name_plural = "Section Report Publications"

    def __str__(self):
        return self.id


class SectionReportUser(Report):
    reported_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, related_name="reported_user")

    class Meta:
        verbose_name = "Section Report User"
        verbose_name_plural = "Section Report Users"

    def __str__(self):
        return self.id
