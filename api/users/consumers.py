import json
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from django.contrib.auth import get_user_model

from .models import NotificationsChannel
from ..users.serializers import BasicUserSerializer

User = get_user_model()
class NotificationsConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None
        self.user_id = None
        self.to_user = None

    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']

        await self.save_user_channel()

        await self.accept()

    async def disconnect(self, close_code):

        await self.delete_user_channel()

        await self.disconnect(close_code)


    async def receive_json(self, text_data=None, byte_data=None):
        title = text_data['title']
        body = text_data['body']
        to_user = text_data['to_user']
        response = {
            'title': title,
            'body': body,
            "type": "send.message"
        }

        to_user_channel, to_user_id = await self.get_user_channel(to_user)
        channel_layer = get_channel_layer()

        await self.channel_layer.group_add(
            str(to_user_id),
            str(self.channel_name)
        )
        if to_user_channel is not None and to_user_id is not None:
            await self.channel_layer.group_add(
                str(to_user_id),
                str(to_user_channel)
            )

        await channel_layer.group_send(
            str(to_user_id), response
        )

    async def send_message(self, event):

        #print(event)

        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_user_channel(self, to_user):
        try:
            channel_name = NotificationsChannel.objects.filter(
                user=to_user).latest('id')
            user_id = channel_name.user.id
        except Exception as e:
            channel_name = None
            user_id = None

        return channel_name, user_id

    @database_sync_to_async
    def save_user_channel(self):
        self.user = User.objects.get(id=self.user_id)

        NotificationsChannel.objects.create(
            user=self.user,
            channel=self.channel_name
        )

    @database_sync_to_async
    def delete_user_channel(self):
        NotificationsChannel.objects.filter(user=self.user).delete()