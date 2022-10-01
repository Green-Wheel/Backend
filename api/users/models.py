from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class LoginMethods(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        verbose_name = "Login Method"
        verbose_name_plural = "Login Methods"

    def __str__(self):
        return self.name

class Languages(models.Model):
    shortname = models.CharField(max_length=3, null=False, blank=False, primary_key=True)
    name = models.CharField(max_length=50, null=False, blank=False)
    class Meta:
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def __str__(self):
        return self.name
class Users(AbstractUser):
    about = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, null=True, blank=True, default=1)
    profile_picture = models.TextField(null=True, blank=True)
    api_key = models.TextField(null=True, blank=True)
    login_method = models.ForeignKey(LoginMethods, on_delete=models.CASCADE, null=True, blank=True, default=1)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username