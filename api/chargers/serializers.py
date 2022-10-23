from rest_framework import serializers
from api.chargers.models import PublicChargers, Chargers, PrivateChargers, ConnectionsType, Localizations, Town, Province, SpeedsType, CurrentsType, Publication

class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ["title", "description", "direction", "town", "localization"]


class LocalizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localizations
        fields = ["latitude", "longitude"]


class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = ["name", "province"]


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ["name"]


class ChargerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chargers
        fields = ["title", "description", "direction", "town", "localization", "speed", "connection_type", "current_type", "power"]


class SpeedTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeedsType
        fields = ["name"]


class connectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionsType
        fields = ["name"]


class CurrentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentsType
        fields = ["name"]


class privateChargerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateChargers
        fields =  ["title", "description", "direction", "town", "localization", "speed", "connection_type", "current_type", "power", "price"]


class PublicChargerSerializer(serializers.ModelSerializer):
    localization = serializers.SerializerMethodField("get_localization")

    def get_localization(self, obj):
        return LocalizationsSerializer(obj.localization).data

    class Meta:
        model = PublicChargers
        fields = ["title", "description", "direction", "town", "localization", "power", "speed", "connection_type",
                  "current_type", "agent", "identifier", "access", "available"]
