from django.forms import forms

from api.chargers.models import Publication
from config import settings
from django.db import models
from api.users.models import Users


class BookingStatus(models.Model):
    name = models.CharField(max_length=20)
    class Meta:
        verbose_name = "BookingStatus"
        verbose_name_plural = "BookingsStatus"
    def __str__(self):
        return self.name

class Bookings(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    publication = models.ForeignKey(to='chargers.Publication', on_delete=models.CASCADE, null=False, blank=False)
    start_date = models.DateTimeField(null=False, blank=False)
    end_date = models.DateTimeField(null=False, blank=False)
    status = models.ForeignKey(to='bookings.BookingStatus', on_delete=models.CASCADE, null=False, blank=False, default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

    def __int__(self):
        return str(self.start_date) + " - " + str(self.end_date)

