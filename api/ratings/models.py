from django.db import models
from config import settings
from api.bookings.models import Bookings
from api.users.models import Users
from api.chargers.models import Publication


# Create your models here.
class Ratings(models.Model):
    id_rating = models.AutoField(primary_key=True)
    rate = models.FloatField(null=False, blank=False)
    comment = models.TextField(null=True, blank=True)
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"

    def __str__(self):
        return self.id_rating


class ClientsRating(Ratings):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)


class PostRating(Ratings):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, null=False, blank=False)
