from django.db.models import Avg
from rest_framework import serializers

from api.bikes.models import Bikes
from api.bikes.services import get_images
from api.chargers.models import Images
from api.chargers.serializers import LocalizationSerializer, TownSerializer, ImageSerializer
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
    images = serializers.SerializerMethodField("get_image")

    def get_localization(self, obj):
        return LocalizationSerializer(obj.localization).data

    def get_town(self, obj):
        return TownSerializer(obj.town).data

    def get_avg_rating(self, obj):
        return PostRating.objects.filter(publication=obj.id).aggregate(Avg('rate'))['rate__avg']

    def get_image(self, obj):
        saved_images = Images.objects.filter(publication=obj.id)
        images = []
        for image in saved_images:
            # img = get_images(image.image_path)
            images.append(ImageSerializer(image).data)
        return images

    class Meta:
        model = Bikes
        fields = ["id", "title", "description", "direction", "localization", "town", "avg_rating", "bike_type", "power",
                  "price", "images"]


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
        fields = ["id", "name"]
