from django.db import models
from api.chargers.models import Publication
from django.conf import settings

from api.ratings.models import Ratings


class ReportReasons(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
class Report(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    reason = models.ForeignKey(ReportReasons, on_delete=models.CASCADE, null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    image = models.URLField(null=True, blank=True)
    date_reported = models.DateTimeField(auto_now_add=True)
    rating = models.ForeignKey(Ratings, on_delete=models.CASCADE, null=True, blank=False)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, null=True, blank=False)
    reported_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=False,
                                      related_name="reported_user")
    closed = models.BooleanField(default=False)


    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
        unique_together = [['user', "rating"], ['user',"publication"], ['user',"reported_user"]]
        # abstract = True

    def __str__(self):
        return str(self.id)


class TypeResolution(models.Model):
    type = models.CharField(max_length=50, null=False, blank=False, unique=True)

    class Meta:
        verbose_name = "Type Resolution"
        verbose_name_plural = "Types Resolution"

    def __str__(self):
        return self.type


class FeedbackReport(models.Model):
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False, related_name="moderator")
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=False, blank=False)
    resolution = models.ForeignKey(TypeResolution, on_delete=models.CASCADE, null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    date_resolution = models.DateTimeField(null=True, blank=True, auto_now_add=True)

    class Meta:
        verbose_name = "Feedback Report"
        verbose_name_plural = "Feedback Reports"

    def __str__(self):
        return str(self.id)

