from django.urls import re_path, path
from .consumers import NotificationsConsumer

notifications_websocket_patterns = [
    path('', NotificationsConsumer.as_asgi())
]