from datetime import datetime

from rest_framework import serializers
from .models import Bookings, BookingStatus
from api.chargers.models import PrivateChargers
from api.users.models import Users
from ..bikes.models import Bikes
from ..publications.models import Publication, OccupationRanges
from ..publications.serializers import PublicationSerializer, PublicationListSerializer
from ..users.serializers import BasicUserSerializer


class BookingStatusSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = BookingStatus
        fields = ["id", "name"]


class BookingsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    publication = serializers.SerializerMethodField('getPublication')
    user = serializers.SerializerMethodField('getUser')
    status = serializers.SerializerMethodField('getStatus')
    created = serializers.DateTimeField(read_only=True)

    def getUser(self, obj):
        try:
            return BasicUserSerializer(Users.objects.get(id=obj.user.id)).data
        except Users.DoesNotExist:
            return None

    def getPublication(self, obj):
        try:
            return PublicationSerializer(Publication.objects.get(id=obj.publication.id), many=False).data
        except Publication.DoesNotExist:
            return None
        except:
            return None

    def getStatus(self, obj):
        try:
            return BookingStatusSerializer(BookingStatus.objects.get(id=obj.status.id)).data
        except BookingStatus.DoesNotExist:
            print("Status does not exist")
            return None

    class Meta:
        model = Bookings
        fields = ["id", "user", "publication", "start_date", "end_date", "status", "created"]


class SimpleBookingsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    publication = serializers.SerializerMethodField('getPublication')
    user = serializers.SerializerMethodField('getUser')

    def getUser(self, obj):
        try:
            return BasicUserSerializer(Users.objects.get(id=obj.user.id)).data
        except Users.DoesNotExist:
            return None

    def getPublication(self, obj):
        try:
            return PublicationListSerializer(Publication.objects.get(id=obj.publication.id), many=False).data
        except Publication.DoesNotExist:
            print("Publication does not exist")
            return None

    class Meta:
        model = Bookings
        fields = ["id", "user", "publication"]


class BookingsEditSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        start_date = attrs['start_date']
        end_date = attrs['end_date']
        publication = Publication.objects.get(id=attrs['publication'].id)
        if start_date > end_date:
            raise serializers.ValidationError("Start date must be before end date")
        if start_date < datetime.now():
            raise serializers.ValidationError("Start date must be in the future")
        if end_date < datetime.now():
            raise serializers.ValidationError("End date must be in the future")
        if start_date == end_date:
            raise serializers.ValidationError("Start date must be different from end date")
        if publication.owner.id == attrs['user'].id:
            raise serializers.ValidationError("You can't book your own publication")
        if PrivateChargers.objects.filter(id=attrs['publication'].id).count() + Bikes.objects.filter(
                id=attrs['publication'].id).count() == 0:
            raise serializers.ValidationError("You cannot book your own publication")
        start_occupations = OccupationRanges.objects.filter(start_date__gte=attrs["start_date"],
                                                            start_date__lte=attrs["end_date"],related_publication_id=attrs["publication"].id)
        end_occupations = OccupationRanges.objects.filter(end_date__gte=attrs["start_date"],
                                                          end_date__lte=attrs["end_date"],related_publication_id=attrs["publication"].id)
        if start_occupations or end_occupations:
            raise serializers.ValidationError("Publication is already booked for the selected dates")
        return attrs

    class Meta:
        model = Bookings
        fields = ["id", "user", "publication", "start_date", "end_date", "status",
                  "created"]
