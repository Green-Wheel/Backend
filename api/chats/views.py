from django.shortcuts import render
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from api.chargers.pagination import PaginationHandlerMixin
from api.chats.serializers import ChatRoomSerializer, ChatRoomMessageSerializer
from api.chats.services import get_all_chat_rooms_user, get_chat_room_by_id, remove_user_from_chat, \
    get_chat_room_by_id_messages, get_unread_chat_rooms_user, set_readed_chat_rooms_user
from api.users.permissions import SessionAuth, Check_API_KEY_Auth


# Create your views here.
class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'
class ChatsApiView(APIView, PaginationHandlerMixin):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
    pagination_class = BasicPagination

    def get(self, request):
        try:
            chat_rooms = get_all_chat_rooms_user(request.user.id)
            page = self.paginate_queryset(chat_rooms)
            if page is not None:
                serializer = ChatRoomSerializer(page, many=True)
                if request.accepted_renderer.media_type == 'text/html':
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.data, status=status.HTTP_200_OK,
                                    content_type='application/json; charset=utf-8')
            serializer = ChatRoomSerializer(chat_rooms, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ConcreteChatApiView(APIView, PaginationHandlerMixin):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
    pagination_class = BasicPagination

    def get(self, request, user_id):
        try:
            chat_room = get_chat_room_by_id(user_id, request.user.id)
            serializer = ChatRoomSerializer(chat_room)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, chat_id):
        try:
            remove_user_from_chat(chat_id, request.user.id)
            return Response({"res": "Chat room deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ChatRoomMessagesApiView(APIView, PaginationHandlerMixin):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
    pagination_class = BasicPagination

    def get(self, request, user_id):
        try:
            messages = get_chat_room_by_id_messages(user_id, request.user.id)
            page = self.paginate_queryset(messages)
            if page is not None:
                serializer = ChatRoomMessageSerializer(page, many=True)
                if request.accepted_renderer.media_type == 'text/html':
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.data, status=status.HTTP_200_OK,
                                    content_type='application/json; charset=utf-8')
            serializer = ChatRoomMessageSerializer(messages, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UnreadChatsApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

    def get(self, request):
        try:
            unread_chat_rooms = get_unread_chat_rooms_user(request.user.id)
            return Response({"unreads": unread_chat_rooms}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UnreadConcreteChatApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

    def get(self, request, chat_id):
        try:
            set_readed_chat_rooms_user(chat_id,request.user.id)
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)