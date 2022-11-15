from rest_framework import serializers
from .models import Bookings
from api.chargers.models import Publication
from api.users.models import Users
from ..chargers.serializers import PublicationSerializer


class BookingsSerializer(serializers.ModelSerializer):
    publication = serializers.ReadOnlyField(source='publication.id')

    def getPublication(self, publication_id):
        try:
            return PublicationSerializer(Publication.objects.get(id=publication_id),many=False).data
        except Publication.DoesNotExist:
            return None

    class Meta:
        model = Bookings
        fields = ["id", "publication", "start_date", "end_date", "confirmed", "finished", "cancelled",
                  "created"]


class BookingsDetailedSerializer(serializers.ModelSerializer):
    publication = serializers.SerializerMethodField("getPublication")

    def getPublication(self, publication_id):
        try:
            return PublicationSerializer(Publication.objects.get(id=publication_id), many=False).data
        except Publication.DoesNotExist:
            return None

    class Meta:
        model = Bookings
        fields = ["id", "publication", "start_date", "end_date", "confirmed", "finished", "cancelled",
                  "created"]
