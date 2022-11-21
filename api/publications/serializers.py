from rest_framework import serializers

from api.bikes.models import Bikes
from api.bikes.serializers import DetailedBikeSerializer, BikeListSerializer
from api.chargers.models import Chargers, Publication
from api.chargers.serializers import DetailedChargerSerializer, ChargerListSerializer
from api.publications.models import Localizations, Town, Province


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