from django.shortcuts import render
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from .models import Bookings
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import BookingsSerializer
from .services import cancel_booking, get_booking, get_user_bookings, get_owner_bookings, create_booking, \
    confirm_booking
from ..chargers.pagination import PaginationHandlerMixin
from ..users.permissions import Check_API_KEY_Auth, SessionAuth


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'
# Create your views here.
class UserBookingsApiView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
    def get(self, request):
        order = request.query_params.get('orderby', None)
        bookings = get_user_bookings(request.user.id, order)
        page = self.paginate_queryset(bookings)
        if page is not None:
            serializer = BookingsSerializer(page, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
            else:
                return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        else:
            serializer = BookingsSerializer(bookings, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')


    def post(self, request):
        data = request.data
        booking = {"publication": data["publication"], "start_date": data["start_date"], "end_date": data["end_date"],
                   'user': request.user.id, "confirmed": False, "cancelled": False}
        try:
            booking = create_booking(booking)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(BookingsSerializer(booking).data, status=status.HTTP_201_CREATED)
            else:
                return Response(BookingsSerializer(booking).data, status=status.HTTP_201_CREATED,
                                content_type='application/json; charset=utf-8')
        except Exception as e:
            print(e)
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)

class UserHistorialApiView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
    def get(self, request):
        order = request.query_params.get('orderby', None)
        bookings = get_user_bookings(request.user.id, order,'historial')
        page = self.paginate_queryset(bookings)
        if page is not None:
            serializer = BookingsSerializer(page, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
            else:
                return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        else:
            serializer = BookingsSerializer(bookings, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')
class OwnerBookingsApiView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
    def get(self, request):
        booking_type = request.query_params.get('type', None)
        bookings = get_owner_bookings(request.user.id, booking_type)
        page = self.paginate_queryset(bookings)
        if page is not None:
            serializer = BookingsSerializer(page, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
            else:
                return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        else:
            serializer = BookingsSerializer(bookings, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')

class OwnerHistorialBookingsApiView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
    def get(self, request):
        bookings = get_owner_bookings(request.user.id, 'historial')
        page = self.paginate_queryset(bookings)
        if page is not None:
            serializer = BookingsSerializer(page, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
            else:
                return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        else:
            serializer = BookingsSerializer(bookings, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')

class ConcreteBookingApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
    def get(self, request, booking_id):
        try:
            booking = get_booking(booking_id)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(BookingsSerializer(booking).data, status=status.HTTP_200_OK)
            else:
                return Response(BookingsSerializer(booking).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        except:
            return Response(
                {"res": "Booking with the id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
    def put(self, request, booking_id):
        try:
            booking = confirm_booking(booking_id, request.data.get("confirmed"))
            if request.accepted_renderer.media_type == 'text/html':
                return Response(BookingsSerializer(booking).data, status=status.HTTP_200_OK)
            else:
                return Response(BookingsSerializer(booking).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        except Bookings.DoesNotExist:
            return Response(
                {"res": "Booking with the id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"res": e.args[0]},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, booking_id):
        try:
            booking = cancel_booking(booking_id)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(BookingsSerializer(booking).data, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(BookingsSerializer(booking).data, status=status.HTTP_204_NO_CONTENT,
                                content_type='application/json; charset=utf-8')

        except Bookings.DoesNotExist:
            return Response(
                {"res": "Booking with the id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"res": e.args[0]},
                status=status.HTTP_400_BAD_REQUEST
            )
