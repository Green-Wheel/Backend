import random
import string

from api.chargers.models import Publication
from api.users.models import Users
from api.users.serializers import UserSerializer, CreateUserSerializer
from utils.imagesS3 import upload_image_to_s3



def get_user(user_id):
    try:
        user = Users.objects.get(id=user_id)
        if not user.is_active:
            raise Exception("User not active")
        return user
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

def get_user_posts(user_id):
    user = Users.objects.get(id=user_id)
    if not user.is_active:
        raise Exception("User not active")
    return Publication.objects.filter(owner_id=user_id).order_by('-created_at')


def generate_api_key():
    chars = ''.join([string.ascii_letters, string.digits, string.punctuation]).replace('\'', '').replace('"',
                                                                                                         '').replace(
        '\\', '')

    SECRET_KEY = ''.join([random.SystemRandom().choice(chars) for i in range(32)])
    return SECRET_KEY


def password_check(password):
    SpecialSym = ['$', '@', '#', '%']
    val = True

    if len(password) < 6:
        raise ValueError('length should be at least 6')

    if len(password) > 20:
        raise ValueError('length should be not be greater than 8')

    if not any(char.isdigit() for char in password):
        raise ValueError('Password should have at least one numeral')

    if not any(char.isupper() for char in password):
        raise ValueError('Password should have at least one uppercase letter')

    if not any(char.islower() for char in password):
        raise ValueError('Password should have at least one lowercase letter')

    if not any(char in SpecialSym for char in password):
        raise ValueError('Password should have at least one of the symbols $@#')
    if val:
        return val


def create_user(data):
    user = Users()
    password_check(data["password"])
    user.username = data["username"]
    user.email = data["email"]
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.set_password(data["password"])
    user.api_key = generate_api_key()
    if user.is_valid():
        user.save()
        user.api_key = generate_api_key()
        user.save()
        return user

def update_user(data, user_id):
    user_instance = get_user(user_id)
    if not user_instance.is_active:
        raise Exception("User not active")
    if data.get("email", None) is not None and data["email"] != "":
        user_instance.email = data["email"]
    if data.get("first_name", None) is not None and data["first_name"] != "":
        user_instance.first_name = data["first_name"]
    if data.get("last_name", None) is not None and data["last_name"] != "":
        user_instance.last_name = data["last_name"]
    if data.get("about", None) is not None:
        user_instance.about = data["about"]
    if user_instance.is_valid():
        user_instance.save()
        return user_instance
    else:
        raise Exception(user_instance.errors)

def remove_api_key(user_id):
    user = get_user(user_id)
    user.api_key = None
    user.save()
    return True


def login_user(username, password):
    user = Users.objects.get(username=username)
    if not user.is_active:
        raise Exception("User not active")
    if user.check_password(password):
        user.api_key = generate_api_key()
        user.save()
        return user
    else:
        raise Exception("Wrong password")


def upload_images(user_id, images):
    user = get_user(user_id)
    if not user.is_active:
        raise Exception("User not active")
    for file in images.getlist("images"):
        path = "profile/" + str(user_id) + "/" + file.name
        upload_image_to_s3(file, path)
        user = Users.objects.get(id=user_id)
        user.profile_picture = path
        user.save()
    return get_user(user_id)




def change_password(data, user):
    if not user.is_active:
        raise Exception("User not active")
    password_check(data["password"])
    user.set_password(data["password"])
    user.save()
    return True
