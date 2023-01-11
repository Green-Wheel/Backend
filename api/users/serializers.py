from django.db.models import Avg
from rest_framework import serializers
from .models import Users, Trophies
from ..ratings.models import ClientsRating


class FullUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    trophies = serializers.SerializerMethodField("get_trophies")

    def get_trophies(self, obj):
        all_trophies = Trophies.objects.all()
        user_trophies = obj.trophies.all()
        trophies = []
        for trophy in all_trophies:
            if trophy in user_trophies:
                trophies.append({"id": trophy.id, "achieved": True})
            else:
                trophies.append({"id": trophy.id, "achieved": False})
        return trophies

    class Meta:
        model = Users
        fields = ["id", "last_login", "username", "first_name", "last_name", "email", "is_active", "date_joined",
                  "about", "phone", "birthdate", "profile_picture", "language_id", "level", "xp", "selected_car", "trophies"]


class BasicUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Users
        fields = ["id", "username", "first_name", "last_name", "profile_picture"]


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    rating = serializers.SerializerMethodField("get_rating")
    level = serializers.IntegerField(read_only=True)
    xp = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    trophies = serializers.SerializerMethodField("get_trophies")

    def get_trophies(self, obj):
        all_trophies = Trophies.objects.all()
        user_trophies = obj.trophies.all()
        trophies = []
        for trophy in all_trophies:
            if trophy in user_trophies:
                trophies.append({"id": trophy.id, "achieved": True})
            else:
                trophies.append({"id": trophy.id, "achieved": False})
        return trophies

    def get_rating(self, obj):
        return ClientsRating.objects.filter(client=obj.id).aggregate(Avg('rate'))['rate__avg']


    class Meta:
        model = Users

        fields = ["id", "username", "first_name", "last_name", "email","about", "profile_picture", "language_id", "level", "xp",
                  "rating", "selected_car", "trophies"]


class CreateUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        user = Users.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = Users
        fields = ["id", "username", "first_name", "last_name", "email", "password", "level", "xp","api_key"]
