from django.urls import re_path, path
from .consumers import ChatConsumer

chat_websocket_patterns = [
    path('messages/', ChatConsumer.as_asgi())
]