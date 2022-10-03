from django.db import models

from config import settings


# Create your models here.
class Ratings(models.Model):
    rate = models.IntegerField(null=False, blank=False)
    comment = models.TextField(null=True, blank=True)
    # booking = Associar-ho a una reservaFinalitzada (veure com ho fa qui faci el model de reserva)

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
        abstract = True

    def __str__(self):
        return self.id


class ClientsRating(Ratings):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)


# class PostRating(Ratings):
#  post = models.ForeignKey(Post, on_delete=models.CASCADE, null=False, blank=False)
