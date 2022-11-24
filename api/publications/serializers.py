from datetime import datetime

from rest_framework import serializers
from api.bikes.models import Bikes
from api.bikes.serializers import DetailedBikeSerializer, BikeListSerializer
from api.chargers.models import Chargers, Publication
from api.chargers.serializers import DetailedChargerSerializer, ChargerListSerializer
from api.publications.models import Localizations, Town, Province, Images, OccupationRanges, OccupationRepeatMode


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


class PublicationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.SerializerMethodField('get_type')
    charger = serializers.SerializerMethodField('get_charger')
    bike = serializers.SerializerMethodField('get_bike')
    images = serializers.SerializerMethodField("get_image")

    def get_type(self, obj):
        try:
            Chargers.objects.get(id=obj.id)
            return "Charger"
        except Chargers.DoesNotExist:
            return "Bike"

    def get_charger(self, obj):
        try:
            return DetailedChargerSerializer(Chargers.objects.get(id=obj.id)).data
        except Chargers.DoesNotExist:
            return None

    def get_bike(self, obj):
        try:
            return DetailedBikeSerializer(Bikes.objects.get(id=obj.id)).data
        except Bikes.DoesNotExist:
            return None

    def get_image(self, obj):
        saved_images = Images.objects.filter(publication=obj.id)
        images = []
        for image in saved_images:
            images.append(ImageSerializer(image).data)
        return images

    class Meta:
        model = Publication
        fields = ["id", "type", "charger", "bike", "images"]


class PublicationListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    type = serializers.SerializerMethodField('get_type')
    charger = serializers.SerializerMethodField('get_charger')
    bike = serializers.SerializerMethodField('get_bike')

    def get_type(self, obj):
        try:
            Chargers.objects.get(id=obj.id)
            return "Charger"
        except Chargers.DoesNotExist:
            return "Bike"

    def get_charger(self, obj):
        try:
            return DetailedChargerSerializer(Chargers.objects.get(id=obj.id)).data
        except Chargers.DoesNotExist:
            return None

    def get_bike(self, obj):
        try:
            return DetailedBikeSerializer(Bikes.objects.get(id=obj.id)).data
        except Chargers.DoesNotExist:
            return None

    class Meta:
        model = Publication
        fields = ["id", "type", "charger", "bike"]


class ImageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    # image = serializers.SerializerMethodField("get_image")
    #
    # def get_image(self, obj):
    #     img = get_image_from_s3(obj.image_path)
    #     return img

    class Meta:
        model = Images
        fields = ["id", "image_path"]


class OccupationRangeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    def validate(self, attrs):
        occupation_id = None
        if self.instance:
            occupation_id = self.instance.id
        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError("Start date cannot be greater than end date")
        if attrs['start_date'] < attrs['related_publication'].created_at:
            raise serializers.ValidationError("Start date cannot be less than publication date")
        if attrs['start_date'] < datetime.now():
            raise serializers.ValidationError("Start date cannot be less than today")
        if attrs['occupation_range_type'].id == 1 and attrs['booking'] is None:
            raise serializers.ValidationError("Booking is required for a booking occupation range")

        start_occupations = OccupationRanges.objects.filter(start_date__gte=attrs['start_date'],
                                                            start_date__lte=attrs['end_date']).exclude(id=occupation_id)
        end_occupations = OccupationRanges.objects.filter(end_date__gte=attrs['start_date'],
                                                          end_date__lte=attrs['end_date']).exclude(id=occupation_id)
        if start_occupations or end_occupations:
            raise serializers.ValidationError("Occupation range already exists")

        return attrs

    class Meta:
        model = OccupationRanges
        fields = ["id", "start_date", "end_date", "occupation_range_type", "related_publication", "repeat_mode",
                  "booking", "created_at"]

class RepeatModeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = OccupationRepeatMode
        fields = ["id", "name"]