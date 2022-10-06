from django.db import models
from api.users.models import Users
from config import settings


# Create your models here.
class Chats(models.Model):
    text = models.CharField(max_length=1500)
    read = models.BooleanField(default=False)
    date_time_read = models.DateTimeField(blank=True, null=True)
    date_time_sent = models.DateTimeField(auto_now_add=True)
    user_sent = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, related_name='user_sent')
    user_recived = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_recived",  blank=True, null=True)

    class Meta:
        verbose_name = "Chat"
        verbose_name_plural = "Chats"

    def __str__(self):
        return self.text
