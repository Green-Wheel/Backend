import json
import random
import smtplib
import string
from email.headerregistry import Address
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from api.chargers.models import Publication
from api.users.consumers import NotificationsConsumer
from api.users.models import Users, LoginMethods, NotificationsChannel, Trophies
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


def set_user_trophie(user, trophie_id):
    trophie = Trophies.objects.get(id=trophie_id)
    user.trophies.add(trophie)


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
        set_user_trophie(user, 12)
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
        set_user_trophie(user_instance, 11)
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
    for file in images:
        path = "profile/" + str(user_id) + "/" + file.name
        s3_path = upload_image_to_s3(file, path)
        user = Users.objects.get(id=user_id)
        user.profile_picture = s3_path
        user.save()
    return get_user(user_id)


def change_password(data, user):
    if not user.is_active:
        raise Exception("User not active")
    password_check(data["password"])
    user.set_password(data["password"])
    user.save()
    return True


def random_with_N_digits(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return random.randint(range_start, range_end)

def send_recover_mail(user):
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("greenwheelpes@gmail.com", "hnzrfjzksqfequym")
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "GreenWheel: Password recovery code"
    msg['From'] = "greenwheelpes@gmail.com"
    msg['To'] = user.email
    html = "Hi " + user.first_name + "!<br>Your password recovery code is:<b>" + str(user.recover_password_code) + "</b><br>Enter it in the application to restore the password."
    msg.attach(MIMEText(html, 'html'))
    # sending the mail
    s.sendmail("greenwheelpes@gmail.com", user.email, msg.as_string())

    # terminating the session
    s.quit()
def generate_recover_code():
    return random_with_N_digits(6)


def recover_password(username):
    user = Users.objects.get(username=username)
    if not user.is_active:
        raise Exception("User not active")
    if user.login_method.id != 1:
        raise Exception("User not allowed to change password")
    user.recover_password_code = generate_recover_code()
    user.save()
    send_recover_mail(user)
    return user.recover_password_code

def validate_code(username, code):
    user = Users.objects.get(username=username)
    print(code)
    if not user.is_active:
        raise Exception("User not active")
    if user.login_method.id != 1:
        raise Exception("User not allowed to change password")
    if int(user.recover_password_code) == code:
        user.api_key = generate_api_key()
        user.recover_password_code = None
        user.save()
        return user
    else:
        raise Exception("Wrong code")

def create_or_get_google_user(data):
    print(data["id"])
    user = Users.objects.filter(google_id=data["id"], login_method_id=2).first()
    if user is not None:
        user.api_key = generate_api_key()
        user.save()
        return user
    else:
        user = Users()
        user.username = data["email"].split("@")[0]
        user.email = data["email"]
        user.first_name = data["displayName"].split(" ")[0]
        user.last_name = data["displayName"].split(" ")[1]
        user.login_method = LoginMethods.objects.get(id=2)
        user.password = "google"
        user.google_id = data["id"]
        user.api_key = generate_api_key()
        if user.is_valid():
            user.save()
            return user
        else:
            raise Exception("User not valid")

def create_or_get_raco_user(code):
    try:
        # Get token
        url = "https://api.fib.upc.edu/v2/o/token"
        body = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "apifib://greenwheel",
            "client_id": "7iaeoueYVnCVmABWy7ZsRibk5FsOXivIhBDatNjV",
            "client_secret": "KTdE1JimloThzCe6lGale5gS1O2Pod3EbqqVtP4KMXd4LRGpFMzwptb11Zzxe4VncwQPTGgX3NTNFJRIMm8BCgNlGE79lDgGw8HzcxrEeqLu9BRoPUSrzFqLA9pV4Y4D"
        }
        headers = {
            'Content-Type': "application/x-www-form-urlencoded"
        }
        response = requests.request("POST", url, data=body, headers=headers)
        token = response.json()["access_token"]
        api_call_headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/json'}
        api_call_response = requests.get("https://api.fib.upc.edu/v2/jo/", headers=api_call_headers,
                                         verify=True)
        user_data = json.loads(api_call_response.text)
        username = user_data["username"]
        user = Users.objects.filter(username=username, login_method_id=3).first()
        if user is not None:
            user.api_key = generate_api_key()
            user.save()
            return user
        else:
            user = Users()
            user.username = user_data["username"]
            user.email = user_data["email"]
            user.first_name = user_data["nom"]
            user.last_name = user_data["cognoms"]
            user.login_method = LoginMethods.objects.get(id=3)
            user.password = "raco"
            user.api_key = generate_api_key()
            if user.is_valid():
                user.save()
                return user
            else:
                raise Exception("User not valid")
    except Exception as e:
        print(e)
        raise Exception("No s'ha pogut obtenir la informacio de l'usuari")

def send_notification(to_user, title, body):
    body = {
        "title": title,
        "body": body,
        "type": "send.message"
    }
    channel_layer = get_channel_layer()
    channel_name = get_user_channel(to_user)
    async_to_sync(channel_layer.group_add)(str(to_user), str(channel_name))
    async_to_sync(channel_layer.group_send)(str(to_user), body)

def get_user_channel(to_user):
    try:
        channel_name = NotificationsChannel.objects.filter(
            user=to_user).latest('id')

    except Exception as e:
        channel_name = None


    return channel_name