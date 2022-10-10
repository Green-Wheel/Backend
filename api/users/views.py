from rest_framework import status

from .models import Users
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class LanguageApiView(APIView):
    def get_object(self, user_id):
        try:
            return Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return None

    def langStringToId(self, lang):
        if lang == "ca":
            return 1
        elif lang == "es":
            return 2
        elif lang == "en":
            return 3
        else:
            return None

    def langIdToString(self, lang):
        if lang == 1:
            return "ca"
        elif lang == 2:
            return "es"
        elif lang == 3:
            return "en"
        else:
            return None

    def get(self, request):
        user_id = 1
        user_instance = self.get_object(user_id)
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
        return Response({"language": self.langIdToString(user_instance.language_id)}, status=status.HTTP_200_OK)

    def put(self, request):
        user_id = 1
        user_instance = self.get_object(user_id)
        if not user_instance:
            return Response(
                {"res": "User with the id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        lang = request.data["language"]

        user_instance.language_id = self.langStringToId(lang)
        user_instance.save()
        return Response({"res": "Language changed"}, status=status.HTTP_200_OK)
