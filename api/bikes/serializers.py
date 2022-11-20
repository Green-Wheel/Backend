from django.db.models import Avg
from rest_framework import serializers

from api.bikes.models import Bikes
from api.chargers.serializers import LocalizationSerializer, TownSerializer
from api.ratings.models import PostRating


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

    def get_localization(self, obj):
        return LocalizationSerializer(obj.localization).data

    def get_town(self, obj):
        return TownSerializer(obj.town).data

    def get_avg_rating(self, obj):
        return PostRating.objects.filter(publication=obj.id).aggregate(Avg('rate'))['rate__avg']

    class Meta:
        model = Bikes
        fields = ["id", "title", "description", "direction", "localization", "town", "avg_rating", "bike_type", "power",
                  "price"]


class BikeListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    localization = serializers.SerializerMethodField("get_localization")
    avg_rating = serializers.SerializerMethodField("get_avg_rating")

    def get_localization(self, obj):
        return LocalizationSerializer(obj.localization).data

    def get_avg_rating(self, obj):
        return PostRating.objects.filter(publication=obj.id).aggregate(Avg('rate'))['rate__avg']

    class Meta:
        model = Bikes
        fields = ["id", "title", "localization", "avg_rating", "bike_type", "price"]


class BikeTypeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Bikes
        fields = ["id", "bike_type"]
