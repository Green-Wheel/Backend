from api.chats.models import ChatRoom, ChatRoomParticipants, ChatMessage

def __delete_chat_room_if_empty(chat_id):
    chat_room_participant = ChatRoomParticipants.objects.filter(room__id=chat_id)
    if not chat_room_participant:
        ChatMessage.objects.filter(room__id=chat_id).delete()
        ChatRoom.objects.filter(id=chat_id).delete()
    else:
        ChatRoom.objects.filter(id=chat_id).update(open=False)

def get_all_chat_rooms_user(user_id):
    room_ids = list(ChatRoomParticipants.objects.filter(
        user=user_id).values_list('room__id', flat=True))
    rooms = list(ChatRoomParticipants.objects.exclude(user__id=user_id).filter(
        room__id__in=room_ids).values('room__id',
                                      'room__last_message', 'room__last_sent_user__username', 'room__last_sent_time','user'))
    return rooms

def get_chat_room_by_id(chat_id,user_id):
    chat_room = ChatRoomParticipants.objects.filter(room__id=chat_id).exclude(user__id=user_id).values('room__id',
                                                                        'room__last_message', 'room__last_sent_user__username', 'room__last_sent_time', 'user')
    if chat_room.exists():
        return chat_room.first()
    raise Exception("Chat room not found")

def get_chat_room_by_id_messages(chat_id,user_id):
    user_chat = ChatRoomParticipants.objects.filter(room__id=chat_id, user__id=user_id)
    if user_chat:
        return ChatMessage.objects.filter(room__id=chat_id).order_by('-created_at')

def remove_user_from_chat(chat_id, user_id):
    chat_room_participant = ChatRoomParticipants.objects.filter(room__id=chat_id, user__id=user_id)
    if chat_room_participant:
        chat_room_participant.delete()
        __delete_chat_room_if_empty(chat_id)
    else:
        raise Exception("Chat room not found")
