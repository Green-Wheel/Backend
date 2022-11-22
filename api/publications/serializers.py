from datetime import datetime

from rest_framework import serializers

from api.bikes.models import Bikes
from api.bikes.serializers import DetailedBikeSerializer, BikeListSerializer
from api.chargers.models import Chargers, Publication
from api.chargers.serializers import DetailedChargerSerializer, ChargerListSerializer
from api.publications.models import Localizations, Town, Province, OccupationRanges


class LocalizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localizations
        fields = ["latitude", "longitude"]


class TownSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    province = serializers.SerializerMethodField("get_province")

    def get_province(self, obj):
        return ProvinceSerializer(obj.province).data

    class Meta:
        model = Town
        fields = ["id", "name", "province"]


class ProvinceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Province
        fields = ["id", "name"]


class PublicationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.SerializerMethodField('get_type')
    child = serializers.SerializerMethodField('get_child')

    def get_type(self, obj):
        try:
            Chargers.objects.get(id=obj.id)
            return "Charger"
        except Chargers.DoesNotExist:
            return "Bike"

    def get_child(self, obj):
        try:
            return DetailedChargerSerializer(Chargers.objects.get(id=obj.id)).data
        except Chargers.DoesNotExist:
            return DetailedBikeSerializer(Bikes.objects.get(id=obj.id)).data

    class Meta:
        model = Publication
        fields = ["id", "type", "child"]


class PublicationListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.SerializerMethodField('get_type')
    child = serializers.SerializerMethodField('get_child')

    def get_type(self, obj):
        try:
            Chargers.objects.get(id=obj.id)
            return "Charger"
        except Chargers.DoesNotExist:
            return "Bike"

    def get_child(self, obj):
        try:
            return ChargerListSerializer(Chargers.objects.get(id=obj.id)).data
        except Chargers.DoesNotExist:
            return BikeListSerializer(Bikes.objects.get(id=obj.id)).data

    class Meta:
        model = Publication
        fields = ["id", "type", "child"]


class OccupationRangeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)


    def validate(self, attrs):
        occupation_id = None
        if self.instance:
            occupation_id = self.instance.id
        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError("Start date cannot be greater than end date")
        if attrs['start_date'] < attrs['related_publication'].created_at:
            raise serializers.ValidationError("Start date cannot be less than publication date")
        if attrs['start_date'] < datetime.now():
            raise serializers.ValidationError("Start date cannot be less than today")
        if attrs['occupation_range_type'].id == 1 and attrs['booking'] is None:
            raise serializers.ValidationError("Booking is required for a booking occupation range")

        start_occupations = OccupationRanges.objects.filter(start_date__gte=attrs['start_date'],
                                                            start_date__lte=attrs['end_date']).exclude(id=occupation_id)
        end_occupations = OccupationRanges.objects.filter(end_date__gte=attrs['start_date'],
                                                          end_date__lte=attrs['end_date']).exclude(id=occupation_id)
        if start_occupations or end_occupations:
            raise serializers.ValidationError("Occupation range already exists")

        return attrs

    class Meta:
        model = OccupationRanges
        fields = ["id", "start_date", "end_date", "occupation_range_type", "related_publication", "repeat_mode",
                  "booking", "created_at"]
