import json
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from django.contrib.auth import get_user_model

from .models import ChatRoom, ChatRoomParticipants, ChatMessage, ChatParticipantsChannel
from ..users.models import Trophies
from ..users.serializers import BasicUserSerializer
from ..users.services import send_notification, send_notification_async

User = get_user_model()


def set_message_trophie(user):
    trophie = Trophies.objects.get(id=10)
    user.trophies.add(trophie)
    user.level = user.trophies.count()
    user.save()


class ChatConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.user_id = None
        self.to_user = None
        self.chatroom_id = None

    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']

        await self.save_user_channel()

        await self.accept()

    async def disconnect(self, close_code):

        await self.delete_user_channel()

        await self.disconnect(close_code)

    async def receive_json(self, text_data=None, byte_data=None):
        message = text_data['message']
        self.to_user = text_data['to_user']
        to_user_channel, to_user_id = await self.get_user_channel(self.to_user)
        message_response = await self.save_message(self.to_user, self.user, message)
        message_response['type'] = 'send.message'

        channel_layer = get_channel_layer()

        await self.channel_layer.group_add(
            str(self.chatroom_id),
            str(self.channel_name)
        )
        if to_user_channel is not None and to_user_id != None:
            await self.channel_layer.group_add(
                str(self.chatroom_id),
                str(to_user_channel)
            )

        await channel_layer.group_send(
            str(self.chatroom_id), message_response
        )

        await send_notification_async(self.to_user, "Tienes un nuevo mensaje!", self.user.username + ": " + message)

    async def send_message(self, event):

        # print(event)

        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_user_channel(self, to_user):
        try:
            channel_name = ChatParticipantsChannel.objects.filter(
                user=to_user).latest('id')
            user_id = channel_name.user.id
        except Exception as e:
            channel_name = None
            user_id = None

        return channel_name, user_id

    @database_sync_to_async
    def save_user_channel(self):
        self.user = User.objects.get(id=self.user_id)

        ChatParticipantsChannel.objects.create(
            user=self.user,
            channel=self.channel_name
        )

    @database_sync_to_async
    def delete_user_channel(self):
        ChatParticipantsChannel.objects.filter(user=self.user).delete()

    @database_sync_to_async
    def save_message(self, to_user_id, user, message):

        room_ids = list(ChatRoomParticipants.objects.filter(
            user=user.id).values_list('room__id', flat=True))
        chat_participant = ChatRoomParticipants.objects.filter(user__id=to_user_id).filter(
            room__id__in=room_ids).first()
        if chat_participant:
            chatroom = ChatRoom.objects.get(id=chat_participant.latest('id').room.id)
            chat_participant.unread=True
            chat_participant.save()
        else:
            chatroom = ChatRoom.objects.create()
            ChatRoomParticipants.objects.create(user=user, room=chatroom,unread=False)
            ChatRoomParticipants.objects.create(user_id=to_user_id, room=chatroom, unread=True)

        self.chatroom_id = chatroom.id

        chatroom.last_message = message
        chatroom.last_sent_user = self.user
        chatroom.save()

        message = ChatMessage.objects.create(
            room=chatroom, user=self.user, content=message
        )

        message_response = {
            'id': message.id,
            'room_id': chatroom.id,
            'content': message.content,
            'sender': BasicUserSerializer(message.user).data,
            'created_at': str(message.created_at),
        }

        set_message_trophie(user)

        return message_response
