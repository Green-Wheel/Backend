from config import settings
from django.db import models
from api.users.models import Users
from api.chargers.models import Publication



class Bookings(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, blank=False)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, null=False, blank=False)
    start_date = models.DateTimeField(null=False, blank=False)
    end_date = models.DateTimeField(null=False, blank=False)
    confirmed = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    cancelled = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"

