from rest_framework import serializers
from api.chargers.models import PublicChargers, Chargers, PrivateChargers, ConnectionsType, Localizations, Town, \
    Province, SpeedsType, CurrentsType, Publication


class PublicationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    localization = serializers.SerializerMethodField("get_localization")
    town = serializers.SerializerMethodField("get_town")

    def get_localization(self, obj):
        return LocalizationSerializer(obj.localization).data

    def get_town(self, obj):
        return TownSerializer(obj.town).data
    class Meta:
        model = Publication
        fields = ["id","title", "description", "direction", "town", "localization"]


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
        fields = ["id","name", "province"]


class ProvinceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Province
        fields = ["id","name"]


class ChargerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    localization = serializers.SerializerMethodField("get_localization")
    town = serializers.SerializerMethodField("get_town")
    connection_type = serializers.SerializerMethodField("get_connection")
    current_type = serializers.SerializerMethodField("get_current")
    speed = serializers.SerializerMethodField("get_speed")
    charger_type = serializers.SerializerMethodField("get_type")
    child = serializers.SerializerMethodField("get_child")

    def get_localization(self, obj):
        return LocalizationSerializer(obj.localization).data

    def get_town(self, obj):
        return TownSerializer(obj.town).data

    def get_connection(self, obj):
        connections = []
        for connection in obj.connection_type.all():
            connections.append(connectionTypeSerializer(connection).data)
        return connections

    def get_current(self, obj):
        currents = []
        for current in obj.current_type.all():
            currents.append(CurrentTypeSerializer(current).data)
        return currents

    def get_speed(self, obj):
        speeds = []
        for speed in obj.speed.all():
            speeds.append(SpeedTypeSerializer(speed).data)
        return speeds

    def get_type(self, obj):
        try:
            PublicChargers.objects.get(pk=obj.id)
            return "public"
        except:
            return "private"

    def get_child(self, obj):
        try:
            public_charger = PublicChargers.objects.get(pk=obj.id)
            return PublicChargerSerializer(public_charger).data
        except:
            private_charger = PrivateChargers.objects.get(pk=obj.id)
            return PrivateChargerSerializer(private_charger).data

    class Meta:
        model = Chargers
        fields = ["id","title", "description", "direction", "town", "localization", "speed", "connection_type",
                  "current_type", "power", "charger_type", "child"]


class SpeedTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = SpeedsType
        fields = ["id","name"]


class connectionTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = ConnectionsType
        fields = ["id","name"]


class CurrentTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = CurrentsType
        fields = ["id","name"]


class PrivateChargerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    localization = serializers.SerializerMethodField("get_localization")
    town = serializers.SerializerMethodField("get_town")
    connection_type = serializers.SerializerMethodField("get_connection")
    current_type = serializers.SerializerMethodField("get_current")
    speed = serializers.SerializerMethodField("get_speed")

    def get_localization(self, obj):
        return LocalizationSerializer(obj.localization).data

    def get_town(self, obj):
        return TownSerializer(obj.town).data

    def get_connection(self, obj):
        connections = []
        for connection in obj.connection_type.all():
            connections.append(connectionTypeSerializer(connection).data)
        return connections

    def get_current(self, obj):
        currents = []
        for current in obj.current_type.all():
            currents.append(CurrentTypeSerializer(current).data)
        return currents

    def get_speed(self, obj):
        speeds = []
        for speed in obj.speed.all():
            speeds.append(SpeedTypeSerializer(speed).data)
        return speeds
    class Meta:
        model = PrivateChargers
        fields = ["id","title", "description", "direction", "town", "localization", "speed", "connection_type",
                  "current_type", "power", "price"]


class PublicChargerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    localization = serializers.SerializerMethodField("get_localization")
    town = serializers.SerializerMethodField("get_town")
    connection_type = serializers.SerializerMethodField("get_connection")
    current_type = serializers.SerializerMethodField("get_current")
    speed = serializers.SerializerMethodField("get_speed")

    def get_localization(self, obj):
        return LocalizationSerializer(obj.localization).data

    def get_town(self, obj):
        return TownSerializer(obj.town).data

    def get_connection(self, obj):
        connections = []
        for connection in obj.connection_type.all():
            connections.append(connectionTypeSerializer(connection).data)
        return connections

    def get_current(self, obj):
        currents = []
        for current in obj.current_type.all():
            currents.append(CurrentTypeSerializer(current).data)
        return currents

    def get_speed(self, obj):
        speeds = []
        for speed in obj.speed.all():
            speeds.append(SpeedTypeSerializer(speed).data)
        return speeds

    class Meta:
        model = PublicChargers
        fields = ["id", "description", "direction", "town", "localization", "power", "speed", "connection_type",
                  "current_type", "agent", "identifier", "access", "available"]
