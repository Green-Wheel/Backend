from rest_framework import serializers

from api.chats.models import ChatRoom, ChatMessage, ChatRoomParticipants
from api.users.models import Users
from api.users.serializers import BasicUserSerializer


class ChatRoomSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='room__id')
    last_message = serializers.CharField(source='room__last_message')
    last_sent_user = serializers.CharField(source='room__last_sent_user__username')
    last_sent_time = serializers.DateTimeField(source='room__last_sent_time')
    to_user = serializers.SerializerMethodField("get_user")
    unread = serializers.SerializerMethodField("get_unread")

    def get_user(self, obj):
        return BasicUserSerializer(Users.objects.get(id=obj["user"])).data

    def get_unread(self, obj):
        return ChatRoomParticipants.objects.filter(room__id=obj["room__id"]).exclude(user__id=obj["user"]).first().unread

    class Meta:
        model = ChatRoom
        fields = ["id", "to_user", "last_message", "last_sent_user","last_sent_time", "open","unread"]

class ChatRoomMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ["id","sender", "content", "created_at"]