from django.db.models import Avg
from rest_framework import serializers

from .models import Users
from ..ratings.models import ClientsRating


class FullUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "last_login", "username", "first_name", "last_name", "email", "is_active", "date_joined",
                  "about", "phone", "birthdate", "profile_picture", "language_id", "level", "xp"]


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id", "username", "first_name", "last_name", "profile_picture"]

class UserSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField("get_rating")

    def get_rating(self, obj):
        return ClientsRating.objects.filter(client=obj.id).aggregate(Avg('rate'))['rate__avg']

    class Meta:
        model = Users
        fields = ["id", "username", "first_name", "last_name", "about", "profile_picture", "language_id", "level", "xp",
                  "rating"]
