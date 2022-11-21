from django.db.models import Avg
from rest_framework import serializers

from api.bikes.models import Bikes

from api.chargers.models import PublicChargers, Chargers, PrivateChargers, ConnectionsType, SpeedsType, CurrentsType
from api.publications.models import Localizations, Province, Town
from api.chargers.models import PublicChargers, Chargers, PrivateChargers, ConnectionsType, Localizations, Town, \
    Province, SpeedsType, CurrentsType, Publication, Images
from api.ratings.models import PostRating
from api.users.serializers import BasicUserSerializer
from utils.imagesS3 import get_image_from_s3


class PublicationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.SerializerMethodField('get_type')
    child = serializers.SerializerMethodField('get_child')

    def get_localization(self, obj):
        return LocalizationSerializer(obj.localization).data

    def get_town(self, obj):
        return TownSerializer(obj.town).data

    def get_type(self, obj):
        try:
            return "Charger"
        except Chargers.DoesNotExist:
            return "Bike"

    def get_child(self, obj):
        try:
            return DetailedChargerSerializer(Chargers.objects.get(id=obj.id)).data
        except Chargers.DoesNotExist:
            return None

    class Meta:
        model = Publication
        fields = ["id", "type", "child"]


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


class ChargerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    localization = serializers.SerializerMethodField("get_localization")
    charger_type = serializers.SerializerMethodField("get_type")

    def get_localization(self, obj):
        return LocalizationSerializer(obj.localization).data

    def get_type(self, obj):
        try:
            PublicChargers.objects.get(pk=obj.id)
            return "public"
        except:
            return "private"

    class Meta:
        model = Chargers
        fields = ["id", "localization", "charger_type"]


class ChargerListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    localization = serializers.SerializerMethodField("get_localization")
    connection_type = serializers.SerializerMethodField("get_connection")
    avg_rating = serializers.SerializerMethodField("get_avg_rating")
    charger_type = serializers.SerializerMethodField("get_type")
    child = serializers.SerializerMethodField("get_child")

    def get_localization(self, obj):
        return LocalizationSerializer(obj.localization).data

    def get_connection(self, obj):
        connections = []
        for connection in obj.connection_type.all():
            connections.append(ConnectionTypeSerializer(connection).data)
        return connections

    def get_avg_rating(self, obj):
        return PostRating.objects.filter(publication=obj.id).aggregate(Avg('rate'))['rate__avg']

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
        fields = ["id", "title", "localization", "connection_type", "avg_rating", "charger_type", "child"]


class DetailedChargerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    localization = serializers.SerializerMethodField("get_localization")
    town = serializers.SerializerMethodField("get_town")
    connection_type = serializers.SerializerMethodField("get_connection")
    current_type = serializers.SerializerMethodField("get_current")
    speed = serializers.SerializerMethodField("get_speed")
    avg_rating = serializers.SerializerMethodField("get_avg_rating")
    charger_type = serializers.SerializerMethodField("get_type")
    child = serializers.SerializerMethodField("get_child")

    def get_localization(self, obj):
        return LocalizationSerializer(obj.localization).data

    def get_town(self, obj):
        return TownSerializer(obj.town).data

    def get_connection(self, obj):
        connections = []
        for connection in obj.connection_type.all():
            connections.append(ConnectionTypeSerializer(connection).data)
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

    def get_avg_rating(self, obj):
        return PostRating.objects.filter(publication=obj.id).aggregate(Avg('rate'))['rate__avg']

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
        fields = ["id", "title", "description", "direction", "town", "localization", "speed", "connection_type",
                  "current_type", "power", "avg_rating", "charger_type", "child"]


class PrivateChargerSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField("get_owner")
    images = serializers.SerializerMethodField("get_image")

    def get_owner(self, obj):
        return BasicUserSerializer(obj.owner).data

    def get_image(self, obj):
        saved_images = Images.objects.filter(publication=obj.id)
        images = []
        for image in saved_images:
            images.append(ImageSerializer(image).data)
        return images

    class Meta:
        model = PrivateChargers
        fields = ["price", "owner", "images"]


class PublicChargerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicChargers
        fields = ["agent", "identifier", "access"]


class SpeedTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = SpeedsType
        fields = ["id", "name"]


class ConnectionTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ConnectionsType
        fields = ["id", "name"]


class CurrentTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CurrentsType
        fields = ["id", "name"]


class ImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    image = serializers.SerializerMethodField("get_image")

    def get_image(self, obj):
        img = get_image_from_s3(obj.image_path)
        return img

    class Meta:
        model = Images
        fields = ["id", "image_path", "image"]





"""class FullPrivateChargerSerializer(serializers.ModelSerializer):
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
            connections.append(ConnectionTypeSerializer(connection).data)
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
        fields = ["id", "title", "description", "direction", "town", "localization", "speed", "connection_type",
                  "current_type", "power", "price"]
"""

"""
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
            connections.append(ConnectionTypeSerializer(connection).data)
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
                  "current_type", "agent", "identifier", "access"]"""
