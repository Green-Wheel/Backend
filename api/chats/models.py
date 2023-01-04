from django.contrib.auth import get_user_model
from django.db import models
from api.users.models import Users
from config import settings

User = get_user_model()
# Create your models here

class ChatParticipantsChannel(models.Model):
    channel = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.channel)

class ChatRoom(models.Model):
    last_message = models.CharField(max_length=1024, null=True)
    last_sent_user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True)
    last_sent_time = models.DateTimeField(auto_now=True)
    open = models.BooleanField(default=True)

    def __str__(self):
        return self.last_message


class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    content = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content


class ChatRoomParticipants(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    room = models.ForeignKey(ChatRoom, on_delete=models.PROTECT)