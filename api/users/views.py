from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Users
from rest_framework.views import APIView
from rest_framework.response import Response

from .permissions import Check_API_KEY_Auth, SessionAuth
from .serializers import UserSerializer
from .services import get_user, langIdToString, update_language, update_user, get_user_posts, create_user, \
    remove_api_key, login_user, change_password, recover_password, validate_code, create_or_get_google_user, \
    create_or_get_raco_user, send_notification
from ..chargers.pagination import PaginationHandlerMixin
from ..publications.serializers import PublicationListSerializer
from .services import get_user, langIdToString, update_language, update_user, upload_images


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'


# Create your views here.
class UserApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

    def get(self, request):
        user = get_user(request.user.id)
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.accepted_renderer.media_type == 'text/html':
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        else:
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK,
                            content_type='application/json; charset=utf-8')

    def put(self, request):
        try:
            user = update_user(request.data, request.user.id)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
            else:
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        except Exception as e:
            if request.accepted_renderer.media_type == 'text/html':
                return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST,
                                content_type='application/json; charset=utf-8')


class ConcreteUserApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

    def get(self, request, user_id):
        try:
            user = get_user(user_id)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
            else:
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LanguageApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

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
        if request.accepted_renderer.media_type == 'text/html':
            return Response({"language": langIdToString(user_instance.language_id)}, status=status.HTTP_200_OK)
        else:
            return Response({"language": langIdToString(user_instance.language_id)}, status=status.HTTP_200_OK,
                            content_type='application/json; charset=utf-8')

    def put(self, request):
        try:
            lang = request.data["language"]
            updated = update_language(lang, request.user.id)
            if not updated:
                return Response(
                    {"res": "User with the id doesn't exist"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            return Response({"res": "Language changed"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UploadProfileImageApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

    def post(self, request):
        try:
            charger = upload_images(request.user.id, request.FILES.getlist('file'))
            if request.accepted_renderer.media_type == 'text/html':
                return Response(UserSerializer(charger).data, status=status.HTTP_200_OK)
            else:
                return Response(UserSerializer(charger).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserPostsApiView(APIView, PaginationHandlerMixin):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
    pagination_class = BasicPagination

    def get(self, request, user_id):
        try:
            posts = get_user_posts(user_id)
            page = self.paginate_queryset(posts)
            if page is not None:
                serializer = PublicationListSerializer(page, many=True)
                if request.accepted_renderer.media_type == 'text/html':
                    return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
                else:
                    return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK,
                                    content_type='application/json; charset=utf-8')
            else:
                serializer = PublicationListSerializer(posts, many=True)
                if request.accepted_renderer.media_type == 'text/html':
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.data, status=status.HTTP_200_OK,
                                    content_type='application/json; charset=utf-8')
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
            if request.accepted_renderer.media_type == 'text/html':
                return Response({"apikey": user.api_key}, status=status.HTTP_201_CREATED)
            else:
                return Response({"apikey": user.api_key}, status=status.HTTP_201_CREATED,
                                content_type='application/json; charset=utf-8')
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RecoverPasswordApiView(APIView):
    authentication_classes = ()

    def get(self, request):
        try:
            code = recover_password(request.query_params["username"])
            return Response(status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            user = validate_code(request.data["username"], request.data["code"])
            login(request, user)
            return Response({"apikey": user.api_key}, status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

    def put(self, request):
        try:
            change_password(request.data, request.user)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

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


class GoogleLoginCallbackApiView(APIView):
    authentication_classes = ()

    def post(self,request):
        try:
            user = create_or_get_google_user(request.data)
            login(request, user)
            return Response({"apikey": user.api_key}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
class RacoLoginCallbackApiView(APIView):
    def post(self,request):
        try:
            user = create_or_get_raco_user(request.data["code"])
            login(request, user)
            return Response({"apikey": user.api_key}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SendNotificationTest(APIView):
    def get(self, request, user_id):
        try:
            send_notification(user_id,"Title","Body")
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)