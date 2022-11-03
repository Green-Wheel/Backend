from rest_framework import serializers

from .models import Users
class NameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = ["id", "last_login",  "username", "first_name", "last_name", "email", "is_active", "date_joined", "about", "phone", "birthdate", "profile_picture", "language_id", "level", "xp"]