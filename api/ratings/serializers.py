from rest_framework import serializers
from .models import Ratings
from api.bookings.models import Bookings


class RatingsSerializer(serializers.ModelSerializer):
    booking = serializers.ReadOnlyField(source='booking.id')

    def getBooking(self, booking_id):
        try:
            return Bookings.objects.get(id=booking_id)
        except Bookings.DoesNotExist:
            return None

    class Meta:
        model = Ratings
        fields = ["id", "rate", "comment", "booking"]
