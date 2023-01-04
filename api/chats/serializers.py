from rest_framework import serializers

from api.chats.models import ChatRoom, ChatMessage
from api.users.models import Users
from api.users.serializers import BasicUserSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='room__id')
    last_message = serializers.CharField(source='room__last_message')
    last_sent_user = serializers.CharField(source='room__last_sent_user__username')
    last_sent_time = serializers.DateTimeField(source='room__last_sent_time')
    user = serializers.SerializerMethodField("get_user")

    def get_user(self, obj):
        return BasicUserSerializer(Users.objects.get(id=obj['user'])).data

    class Meta:
        model = ChatRoom
        fields = ["id", "user", "last_message", "last_sent_user","last_sent_time", "open"]

class ChatRoomMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ["user", "content", "created_at"]