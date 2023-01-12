from django.db.models import Avg
from rest_framework import serializers
from api.bikes.models import Bikes, BikeTypes
from api.chargers.serializers import LocalizationSerializer, TownSerializer
from api.publications.models import Images, Contamination
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
    images = serializers.SerializerMethodField("get_image")
    contamination = serializers.SerializerMethodField("get_contamination")

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

    def get_image(self, obj):
        saved_images = Images.objects.filter(publication=obj.id)
        images = []
        for image in saved_images:
            images.append(ImageSerializer(image).data)
        return images

    def get_contamination(self,obj):
        try:
            return Contamination.objects.get(publication=obj.id).contamination
        except:
            return None

    class Meta:
        model = Bikes
        fields = ["id", "title", "description", "direction", "localization", "town", "avg_rating", "bike_type", "power",
                  "price", "owner", "contamination", "images"]


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


class ImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Images
        fields = ["id", "image_path"]