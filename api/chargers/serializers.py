from rest_framework import serializers

from api.chargers.models import PublicChargers, Localizations


class LocalizationsSerializer(serializers.ModelSerializer):
    class Meta:
        model =Localizations
        fields = ["latitude", "longitude"]


class PublicChargerSerializer(serializers.ModelSerializer):
    localization = serializers.SerializerMethodField("get_localization")

    def get_localization(self, obj):
        return LocalizationsSerializer(obj.localization).data

    class Meta:
        model = PublicChargers
        fields = ["title", "description", "direction", "town", "localization", "power", "speed", "connection_type",
                  "current_type", "agent", "identifier", "access", "available"]
