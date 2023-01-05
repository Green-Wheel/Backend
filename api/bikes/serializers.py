from django.db.models import Avg
from rest_framework import serializers
from api.bikes.models import Bikes, BikeTypes
from api.chargers.serializers import LocalizationSerializer, TownSerializer
from api.ratings.models import PostRating
from api.users.serializers import BasicUserSerializer


class BikeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    localization = serializers.SerializerMethodField("get_localization")

    def get_localization(self, obj):
        return LocalizationSerializer(obj.localization).data

    class Meta:
        model = Bikes
        fields = ["id", "localization", "bike_type"]


class DetailedBikeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    localization = serializers.SerializerMethodField("get_localization")
    town = serializers.SerializerMethodField("get_town")
    avg_rating = serializers.SerializerMethodField("get_avg_rating")
    bike_type = serializers.SerializerMethodField("get_bike_type")
    owner = serializers.SerializerMethodField("get_owner")

    def get_owner(self, obj):
        return BasicUserSerializer(obj.owner).data

    def get_localization(self, obj):
        return LocalizationSerializer(obj.localization).data

    def get_town(self, obj):
        return TownSerializer(obj.town).data

    def get_avg_rating(self, obj):
        return PostRating.objects.filter(publication=obj.id).aggregate(Avg('rate'))['rate__avg']

    def get_bike_type(self, obj):
        return BikeTypeSerializer(obj.bike_type).data

    class Meta:
        model = Bikes
        fields = ["id", "title", "description", "direction", "localization", "town", "avg_rating", "bike_type", "power",
                  "price", "owner"]


class BikeListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    localization = serializers.SerializerMethodField("get_localization")
    avg_rating = serializers.SerializerMethodField("get_avg_rating")
    bike_type = serializers.SerializerMethodField("get_bike_type")
    owner = serializers.SerializerMethodField("get_owner")

    def get_owner(self, obj):
        return BasicUserSerializer(obj.owner).data
    def get_localization(self, obj):
        return LocalizationSerializer(obj.localization).data

    def get_avg_rating(self, obj):
        return PostRating.objects.filter(publication=obj.id).aggregate(Avg('rate'))['rate__avg']

    def get_bike_type(self, obj):
        return BikeTypeSerializer(obj.bike_type).data

    class Meta:
        model = Bikes
        fields = ["id", "title", "localization", "avg_rating", "bike_type", "price", "owner"]


class BikeTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = BikeTypes
        fields = ["id", "name"]
