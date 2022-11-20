from api.users.models import Users
from api.users.serializers import UserSerializer


def get_user(user_id):
    try:
        return Users.objects.get(id=user_id)
    except Users.DoesNotExist:
        return None


def langStringToId(lang):
    if lang == "ca":
        return 1
    elif lang == "es":
        return 2
    elif lang == "en":
        return 3
    else:
        return None


def langIdToString(lang):
    if lang == 1:
        return "ca"
    elif lang == 2:
        return "es"
    elif lang == 3:
        return "en"
    else:
        return None


def update_language(language, user_id):
    user_instance = get_user(user_id)
    if not user_instance:
        return False
    user_instance.language_id = langStringToId(language)
    user_instance.save()
    return True


def update_user(data, user_id):
    user_instance = get_user(user_id)
    user = UserSerializer(user_instance,data=data)
    if user.is_valid():
        user.save()
        return user
    else:
        raise Exception(user.errors)
