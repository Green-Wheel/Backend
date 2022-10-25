from django.db import models
from config import settings
from api.bookings.models import Bookings, FinishedBookings
from api.users.models import Users
from api.chargers.models import Publication


# Create your models here.
class Ratings(models.Model):
    rate = models.FloatField(null=False, blank=False)
    comment = models.TextField(null=True, blank=True)
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE, null=False, blank=False)  # finished_bookings

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"

    def __int__(self):
        return self.id


"""
class PostRating(Ratings):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, null=False, blank=False)


class ClientsRating(Ratings):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)"""
