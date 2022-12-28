from rest_framework import serializers

from api.chargers.serializers import CurrentTypeSerializer
from api.users.serializers import BasicUserSerializer
from api.vehicles.models import CarsModel, CarsBrand, Cars


class CarsBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarsBrand
        fields = ["name"]


class CarsModelSerializer(serializers.ModelSerializer):
    car_brand = serializers.SerializerMethodField("get_car_brand")
    current_type = serializers.SerializerMethodField("get_charger_type")

    def get_car_brand(self, obj):
        return CarsBrandSerializer(obj.car_brand).data

    def get_charger_type(self, obj):
        currents = []
        for current in obj.current_type.all():
            currents.append(CurrentTypeSerializer(current).data.name)
        return currents

    class Meta:
        model = CarsModel
        fields = ["name", "year", "autonomy", "car_brand", "current_type", "consumption"]


class CarsSerializer(serializers.ModelSerializer):
    model = serializers.SerializerMethodField("get_model")
    car_owner = serializers.SerializerMethodField("get_car_owner")

    def get_model(self, obj):
        return CarsModelSerializer(obj.model).data

    def get_car_owner(self, obj):
        return BasicUserSerializer(obj.car_owner).data

    class Meta:
        model = Cars
        fields = ["charge_capacity", "car_license", "model", "car_owner"]
