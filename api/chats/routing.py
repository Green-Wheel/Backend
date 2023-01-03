from django.urls import re_path, path
from .consumers import ChatConsumer

websocket_patterns = [
    path(r'chats/sendmessage/<str:user_id>/', ChatConsumer.as_asgi())
]