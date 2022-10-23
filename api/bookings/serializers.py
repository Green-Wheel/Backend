from rest_framework import serializers
from .models import Bookings
from api.chargers.models import Publication
from api.users.models import Users


class BookingsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    publication = serializers.ReadOnlyField(source='publication.id')

    def getUser(self, user_id):
        try:
            return Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return None

    def getPublication(self, publication_id):
        try:
            return Publication.objects.get(id=publication_id)
        except Publication.DoesNotExist:
            return None

    class Meta:
        model = Bookings
        fields = ["id", "user", "publication", "start_date", "end_date", "confirmed", "finished", "cancelled",
                  "created"]


class BookingsDetailedSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField("getUser")
    publication = serializers.SerializerMethodField("getPublication")

    def getUser(self, user_id):
        try:
            return Users.objects.filter(id=user_id).values()
        except Users.DoesNotExist:
            return None

    def getPublication(self, publication_id):
        try:
            return Publication.objects.filter(id=publication_id).values()
        except Publication.DoesNotExist:
            return None

    class Meta:
        model = Bookings
        fields = ["id", "user", "publication", "start_date", "end_date", "confirmed", "finished", "cancelled",
                  "created"]
