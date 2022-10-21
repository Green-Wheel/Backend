from rest_framework import serializers

"""
class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = "pass"
        fields = []
"""

class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = "__all__"

class LocalizationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localizations
        fields = "__all__"
class TownSerializer(serializers.ModelSerializer):
    class Meta:
        model = Town
        fields = "__all__"

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = "__all__"

class ChargersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chargers
        fields = "__all__"
class SpeedTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeedsType
        fields = "__all__"

class connectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectionsType
        fields = "__all__"

class CurrentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentsType
        fields = "__all__"

class PublicChargersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicChargers
        fields = "__all__"

class privateChargersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivateChargers
        fields = "__all__"
