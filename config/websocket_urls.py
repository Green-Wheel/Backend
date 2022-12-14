from channels.routing import URLRouter
from django.urls import path, include

import api
from api.chats.websocket_urls import chat_websocket_patterns
from api.users.websocket_urls import notifications_websocket_patterns

websocket_patterns = [
    path('ws/<int:user_id>/chats/', URLRouter(chat_websocket_patterns)),
    path('ws/<int:user_id>/notifications/', URLRouter(notifications_websocket_patterns)),
]