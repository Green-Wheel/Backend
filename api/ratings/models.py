from django.db import models
from django.db.models import CheckConstraint, Q

from config import settings
from api.bookings.models import Bookings, FinishedBookings
from api.users.models import Users
from api.chargers.models import Publication


# Create your models here.
class Ratings(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE, null=False, blank=False)  # finished_bookings
    rate = models.FloatField(null=False, blank=False)
    comment = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
        constraints = (CheckConstraint(check=Q(rate__gte=0) & Q(rate__lte=5), name='rate_check'),)

    def __int__(self):
        return self.id


class PostRating(Ratings):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, null=False, blank=False)


class ClientsRating(Ratings):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
