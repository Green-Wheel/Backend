from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.bikes.serializers import BikeSerializer, DetailedBikeSerializer
from api.bikes.services import get_filtered_bikes, create_bike


# Create your views here.
class BikesView(APIView):
    def get(self, request):
        try:
            bikes = get_filtered_bikes(request.query_params)
            serializer = BikeSerializer(bikes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            new_bike = create_bike(request.data, request.user.id)
            # add charger to user
            return Response(DetailedBikeSerializer(new_bike).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)
