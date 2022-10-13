from django.shortcuts import render
from rest_framework import status

from .models import Bookings
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class BookingsApiView(APIView):
    def get(self, request, user_id):
        booking_instance = Bookings.objects.filter(user=user_id)
        if not booking_instance:
            return Response(
                {"res": "Booking with the id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(request, {'bookings': booking_instance})
        # return Response({"booking": booking_instance}, status=status.HTTP_200_OK)
