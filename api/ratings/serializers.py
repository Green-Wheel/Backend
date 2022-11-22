from rest_framework import serializers
from .models import Ratings, PostRating, ClientsRating
from ..users.models import Users
from ..users.serializers import BasicUserSerializer


class RatingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.SerializerMethodField("get_user")

    def get_user(self, obj):
        try:
            return BasicUserSerializer(Users.objects.get(id=obj.user.id)).data
        except Users.DoesNotExist:
            return None
    class Meta:
        model = Ratings
        fields = ["id","user", "rate", "comment", "created_at"]

class PostRatingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = PostRating
        fields = ["id","user", "booking","rate", "comment",  "publication"]
class ClientsRatingSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = ClientsRating
        fields = ["id","user", "booking","rate", "comment", "client"]