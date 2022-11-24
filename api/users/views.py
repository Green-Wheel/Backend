from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from .models import Users
from rest_framework.views import APIView
from rest_framework.response import Response

from .permissions import Check_API_KEY_Auth
from .serializers import UserSerializer
from .services import get_user, langIdToString, update_language, update_user, get_user_posts, create_user, \
    remove_api_key, login_user, change_password
from ..chargers.pagination import PaginationHandlerMixin
from ..publications.serializers import PublicationListSerializer


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'


# Create your views here.
class UserApiView(APIView):
    permission_classes = [Check_API_KEY_Auth]
    def get(self, request):
        user = get_user(request.user.id)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    def put(self, request):
        user = update_user(request.data, request.user.id)
        return Response(user.data, status=status.HTTP_200_OK)


class ConcreteUserApiView(APIView):
    permission_classes = [Check_API_KEY_Auth]
    def get(self, request, user_id):
        try:
            user = get_user(user_id)
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LanguageApiView(APIView):
    permission_classes = [Check_API_KEY_Auth]
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


class UserPostsApiView(APIView, PaginationHandlerMixin):
    permission_classes = [Check_API_KEY_Auth]
    pagination_class = BasicPagination

    def get(self, request, user_id):
        try:
            posts = get_user_posts(user_id)
            page = self.paginate_queryset(posts)
            if page is not None:
                serializer = PublicationListSerializer(page, many=True)
                return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
            else:
                serializer = PublicationListSerializer(posts, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            # return Response(PublicationListSerializer(posts, many=True).data, status=status.HTTP_200_OK)

        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterApiView(APIView):
    authentication_classes = ()
    def post(self, request):
        try:
            user = create_user(request.data)
            login(request, user)
            return Response({"apikey": user.api_key}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RecoverPasswordApiView(APIView):
    authentication_classes = ()
    def get(self, request):
        user = Users.objects.get(email=request.data["email"])
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

    def put(self, request):
        user = Users.objects.get(email=request.data["email"])
        user.set_password(request.data["password"])
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class ChangePasswordApiView(APIView):
    permission_classes = [Check_API_KEY_Auth]
    def put(self, request):
        try:
            change_password(request.data, request.user)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(APIView):
    permission_classes = [Check_API_KEY_Auth]
    authentication_classes = ()
    def post(self, request):
        try:
            remove_api_key(request.user.id)
            logout(request)
            return Response(status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(APIView):
    authentication_classes = ()
    def post(self, request):
        try:
            user = login_user(request.data["username"], request.data["password"])
            login(request, user)
            return Response({"apikey": user.api_key}, status=status.HTTP_201_CREATED)
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
