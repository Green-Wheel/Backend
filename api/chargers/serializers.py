from django.db.models import Avg
from rest_framework import serializers
from api.publications.models import Localizations, Province, Town, Contamination, Images
from api.chargers.models import PublicChargers, Chargers, PrivateChargers, ConnectionsType, SpeedsType, CurrentsType
from api.publications.serializers import ImageSerializer
from api.ratings.models import PostRating
from api.users.models import Users
from api.users.serializers import BasicUserSerializer


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
    public = serializers.SerializerMethodField("get_public")
    private = serializers.SerializerMethodField("get_private")
    contamination = serializers.SerializerMethodField("get_contamination")
    compatible = serializers.SerializerMethodField("get_compatible")
    images = serializers.SerializerMethodField("get_image")

    def get_compatible(self, obj):
        user_id = self.context.get("user_id")
        user = Users.objects.get(id=user_id)
        car = user.selected_car
        if car is not None:
            car_connections = car.model.connection_type.all()
            car_currents = car.model.current_type.all()
            charger_connections = obj.connection_type.all()
            charger_currents = obj.current_type.all()
            connection_compatible = False
            current_compatible = False
            for connection in car_connections:
                if connection in charger_connections:
                    connection_compatible = True
                    break
            ac_dc = CurrentsType.objects.get(name="AC/DC")
            if ac_dc in charger_currents:
                current_compatible = True
            else:
                for current in car_currents:
                    if current in charger_currents:
                        current_compatible = True
                        break
            return connection_compatible and current_compatible
        else:
            return None
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

    def get_public(self, obj):
        try:
            public_charger = PublicChargers.objects.get(pk=obj.id)
            return PublicChargerSerializer(public_charger).data
        except:
            return None

    def get_private(self, obj):
        try:
            private_charger = PrivateChargers.objects.get(pk=obj.id)
            return PrivateChargerSerializer(private_charger).data
        except:
            return None

    def get_contamination(self,obj):
        try:
            return Contamination.objects.get(publication=obj.id).contamination
        except:
            return None

    def get_image(self, obj):
        saved_images = Images.objects.filter(publication=obj.id)
        images = []
        for image in saved_images:
            images.append(ImageSerializer(image).data)
        return images

    class Meta:
        model = Chargers
        fields = ["id", "title", "localization", "connection_type", "avg_rating", "charger_type", "public", "private",
                  "contamination", "compatible", "images"]


class DetailedChargerSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    localization = serializers.SerializerMethodField("get_localization")
    town = serializers.SerializerMethodField("get_town")
    connection_type = serializers.SerializerMethodField("get_connection")
    current_type = serializers.SerializerMethodField("get_current")
    speed = serializers.SerializerMethodField("get_speed")
    avg_rating = serializers.SerializerMethodField("get_avg_rating")
    charger_type = serializers.SerializerMethodField("get_type")
    public = serializers.SerializerMethodField("get_public")
    private = serializers.SerializerMethodField("get_private")
    compatible = serializers.SerializerMethodField("get_compatible")

    def get_compatible(self, obj):
        try:
            user_id = self.context.get("user_id")
            user = Users.objects.get(id=user_id)
            car = user.selected_car
            if car is not None:
                car_connections = car.model.connection_type.all()
                car_currents = car.model.current_type.all()
                charger_connections = obj.connection_type.all()
                charger_currents = obj.current_type.all()
                connection_compatible = False
                current_compatible = False
                for connection in car_connections:
                    if connection in charger_connections:
                        connection_compatible = True
                        break
                ac_dc = CurrentsType.objects.get(name="AC/DC")
                if ac_dc in charger_currents:
                    current_compatible = True
                else:
                    for current in car_currents:
                        if current in charger_currents:
                            current_compatible = True
                            break
                return connection_compatible and current_compatible
            else:
                return None
        except:
            return None

    contamination = serializers.SerializerMethodField("get_contamination")

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

    def get_public(self, obj):
        try:
            public_charger = PublicChargers.objects.get(pk=obj.id)
            return PublicChargerSerializer(public_charger).data
        except:
            return None

    def get_private(self, obj):
        try:
            private_charger = PrivateChargers.objects.get(pk=obj.id)
            return PrivateChargerSerializer(private_charger).data
        except:
            return None

    def get_contamination(self,obj):
        try:
            return Contamination.objects.get(publication=obj.id).contamination
        except:
            return None

    class Meta:
        model = Chargers
        fields = ["id", "title", "description", "direction", "town", "localization", "speed", "connection_type",
                  "current_type", "power", "avg_rating", "charger_type", "public", "private", "contamination",
                  "compatible"]


class PrivateChargerSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField("get_owner")

    def get_owner(self, obj):
        return BasicUserSerializer(obj.owner).data

    class Meta:
        model = PrivateChargers
        fields = ["price", "owner"]


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
