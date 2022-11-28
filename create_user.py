import django.contrib.auth

from config import settings


def create_user():
    user = settings.AUTH_USER_MODEL.objects.create_user('guest', password='guest1234')
    user.api_key = "r}PDN1C(_UJ9!&o,5PT`-y9#}Aaj9QoU"
    user.is_superuser = False
    user.is_staff = False
    user.save()


if __name__ == '__main__':
    create_user()
