from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.bikes.models import Bikes
from api.bikes.serializers import BikeSerializer, DetailedBikeSerializer, BikeListSerializer, BikeTypeSerializer
from api.bikes.services import get_filtered_bikes, create_bike, get_bike_by_id, update_bike, inactive_bike, \
    get_bikes_type, upload_images
from api.chargers.pagination import PaginationHandlerMixin
from api.users.permissions import Check_API_KEY_Auth
from utils import BasicPagination


# Create your views here.
class BikesApiView(APIView):
    permission_classes = [Check_API_KEY_Auth]

    def get(self, request):
        try:
            bikes = get_filtered_bikes(request.query_params)
            serializer = BikeSerializer(bikes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            new_bike = create_bike(request.data, request.user.id)
            # add charger to user
            return Response(DetailedBikeSerializer(new_bike).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BikesListApiView(APIView, PaginationHandlerMixin):
    permission_classes = [Check_API_KEY_Auth]
    pagination_class = BasicPagination

    def get(self, request):
        try:
            bikes = get_filtered_bikes(request.query_params)
            page = self.paginate_queryset(bikes)
            if page is not None:
                serializer = BikeListSerializer(page, many=True)
                return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
            else:
                serializer = BikeListSerializer(bikes, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DetailedBikeApiView(APIView):
    permission_classes = [Check_API_KEY_Auth]

    def get(self, request, bike_id):
        try:
            bike = get_bike_by_id(bike_id)
            return Response(DetailedBikeSerializer(bike).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, bike_id):
        try:
            updated_bike = update_bike(bike_id, request.data, request.user.id)
            return Response(DetailedBikeSerializer(updated_bike).data, status=status.HTTP_200_OK)
        except Bikes.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, bike_id):
        try:
            inactive_bike(bike_id)
            return Response(status=status.HTTP_200_OK)
        except Bikes.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BikeTypesApiView(APIView):
    permission_classes = [Check_API_KEY_Auth]

    def get(self, request):
        try:
            bike_types = get_bikes_type()
            return Response(BikeTypeSerializer(bike_types, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UploadBikeImageApiView(APIView):
    permission_classes = [Check_API_KEY_Auth]

    def post(self, request, bike_id):
        try:
            bike = upload_images(bike_id, request.files)
            return Response(DetailedBikeSerializer(bike).data, status=status.HTTP_200_OK)
        except Bikes.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"res": "Error: " + str(e)},status=status.HTTP_400_BAD_REQUEST)