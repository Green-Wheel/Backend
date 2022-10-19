from rest_framework import serializers

from api.chargers.models import PublicChargers


class PublicChargerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicChargers
        fields = ["title", "description", "direction", "town", "localization", "power", "speed", "connection_type", "current_type", "agent", "identifier", "access", "available"]
