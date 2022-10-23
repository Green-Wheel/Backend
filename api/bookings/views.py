from django.shortcuts import render
from rest_framework import status

from .models import Bookings
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import BookingsSerializer, BookingsDetailedSerializer


# Create your views here.
class BookingsApiView(APIView):
    def get(self, request):
        booking_instance = Bookings.objects.filter(user=1)
        serializer = BookingsDetailedSerializer(booking_instance, many=True)
        if not booking_instance:
            return Response(
                {"res": "Booking with the id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response({"booking": booking_instance}, status=status.HTTP_200_OK)
