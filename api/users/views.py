from rest_framework import status

from .models import Users
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .services import get_user, langIdToString, update_language


# Create your views here.
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
