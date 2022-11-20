from rest_framework import status

from .models import Users
from rest_framework.views import APIView
from rest_framework.response import Response

from .permissions import Check_API_KEY_Auth
from .serializers import UserSerializer
from .services import get_user, langIdToString, update_language, update_user
from ..bikes.services import upload_images


# Create your views here.
class UserApiView(APIView):
    def get(self, request):
        user = get_user(request.user.id)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    def put(self, request):
        user = update_user(request.data, request.user.id)
        return Response(user.data, status=status.HTTP_200_OK)


class ConcreteUserApiView(APIView):
    def get(self, request, user_id):
        try:
            user = get_user(user_id)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LanguageApiView(APIView):
    def get(self, request):
        user_instance = get_user(request.user.id)
        if not user_instance:
            return Response(
                {"res": "User with the id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not user_instance.language_id:
            return Response(
                {"res": "Language not set"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"language": langIdToString(user_instance.language_id)}, status=status.HTTP_200_OK)

    def put(self, request):
        lang = request.data["language"]
        updated = update_language(lang, request.user.id)
        if not updated:
            return Response(
                {"res": "User with the id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"res": "Language changed"}, status=status.HTTP_200_OK)


class UploadProfileImageApiView(APIView):
    permission_classes = [Check_API_KEY_Auth]
    authentication_classes = ()

    def post(self, request):
        try:
            charger = upload_images("profile", request.user.id, request.FILES)
            return Response(UserSerializer(charger).data, status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
