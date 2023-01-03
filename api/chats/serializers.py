from rest_framework import serializers

from api.chats.models import ChatRoom, ChatMessage
from api.users.serializers import BasicUserSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='room_id')
    last_message = serializers.CharField(source='room__last_message')
    last_sent_user = serializers.CharField(source='room__last_sent_user__username')
    user = serializers.SerializerMethodField("get_user")

    def get_user(self, obj):
        return BasicUserSerializer(obj.user).data

    class Meta:
        model = ChatRoom
        fields = ["id", "user", "last_message", "last_sent_user", "open"]

class ChatRoomMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ["user", "content", "created_at"]