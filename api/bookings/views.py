from django.shortcuts import render
from rest_framework import status
from rest_framework.pagination import PageNumberPagination


from .models import Bookings
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import BookingsSerializer
from .services import cancel_booking, get_booking, get_user_bookings, get_owner_bookings, create_booking, \
    confirm_booking
from ..chargers.pagination import PaginationHandlerMixin

class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'
# Create your views here.
class UserBookingsApiView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    def get(self, request):
        order = request.query_params.get('orderby', None)
        bookings = get_user_bookings(request.user.id, order)
        page = self.paginate_queryset(bookings)
        if page is not None:
            serializer = BookingsSerializer(page, many=True)
            return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
        else:
            serializer = BookingsSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        booking = request.data
        booking['user'] = request.user.id
        booking["confirmed"] = False
        booking["cancelled"] = False
        try:
            booking = create_booking(booking)
            return Response(BookingsSerializer(booking).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(e.args[0], status=status.HTTP_400_BAD_REQUEST)


class OwnerBookingsApiView(APIView, PaginationHandlerMixin):
    pagination_class = BasicPagination
    def get(self, request):
        booking_type = request.query_params.get('type', None)
        bookings = get_owner_bookings(request.user.id, booking_type)
        page = self.paginate_queryset(bookings)
        if page is not None:
            serializer = BookingsSerializer(page, many=True)
            return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
        else:
            serializer = BookingsSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class ConcreteBookingApiView(APIView):
    def get(self, request, booking_id):
        try:
            booking = get_booking(booking_id)

            return Response(BookingsSerializer(booking).data, status=status.HTTP_200_OK)
        except:
            return Response(
                {"res": "Booking with the id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
    def put(self, request, booking_id):
        try:
            booking = confirm_booking(booking_id)
            return Response(BookingsSerializer(booking).data, status=status.HTTP_200_OK)
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
            return Response(BookingsSerializer(booking).data, status=status.HTTP_204_NO_CONTENT)

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
