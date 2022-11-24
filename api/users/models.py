import re
from datetime import datetime, timedelta

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
    shortname = models.CharField(max_length=3, null=False, blank=False)
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
    language = models.ForeignKey(Languages, on_delete=models.CASCADE, null=True, blank=True, default=None)
    profile_picture = models.URLField(null=True, blank=False)
    api_key = models.TextField(null=True, blank=True)
    login_method = models.ForeignKey(LoginMethods, on_delete=models.CASCADE, null=True, blank=True, default=1)
    level = models.IntegerField(null=False, blank=False, default=1)
    xp = models.IntegerField(null=False, blank=False, default=0)
    recover_password_code = models.CharField(max_length=6,null=True, blank=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def is_valid(self):
        if not re.findall(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", self.email):
            raise ValueError("Invalid email")
        if not re.findall(r"^[a-zA-Z0-9_.]+$", self.username):
            raise ValueError("Invalid username")
        if not re.findall(r"^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,. '-]+$", self.first_name):
            raise ValueError("Invalid first name")
        if not re.findall(r"^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,. '-]+$", self.last_name):
            raise ValueError("Invalid last name")
        if self.birthdate is not None and self.birthdate >= (datetime.now() - timedelta(days=365 * 16)).date():
            raise ValueError("Invalid birthdate. You must be at least 16 years old")
        return True
