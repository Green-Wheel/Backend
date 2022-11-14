from django.shortcuts import render
from rest_framework import status

from .models import Bookings
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import cancel_booking, get_booking, get_user_bookings, get_owner_bookings


# Create your views here.
class UserBookingsApiView(APIView):
    def get(self, request):
        order = request.query_params.get('orderby', None)
        bookings = get_user_bookings(request.user.id,order)
        return Response(bookings, status=status.HTTP_200_OK)


class OwnerBookingsApiView(APIView):
    def get(self, request):
        booking_type = request.query_params.get('type', None)
        bookings = get_owner_bookings(request.user.id,booking_type)
        return Response(bookings, status=status.HTTP_200_OK)


class ConcreteBookingApiView(APIView):
    def get(self, request, booking_id):
        try:
            booking = get_booking(booking_id)

            return Response(booking, status=status.HTTP_200_OK)
        except:
            return Response(
                {"res": "Booking with the id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, id):
        try:
            booking = cancel_booking(id)
            return Response(booking, status=status.HTTP_204_NO_CONTENT)

        except:
            return Response(
                {"res": "Booking with the id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
