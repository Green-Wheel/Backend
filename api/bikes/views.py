from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.bikes.models import Bikes
from api.bikes.serializers import BikeSerializer, DetailedBikeSerializer, BikeListSerializer, BikeTypeSerializer
from api.bikes.services import get_filtered_bikes, create_bike, get_bike_by_id, update_bike, inactive_bike, \
    get_bikes_type
from api.chargers.pagination import PaginationHandlerMixin
from api.users.permissions import Check_API_KEY_Auth, SessionAuth


class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'


# Create your views here.
class BikesApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

    def get(self, request):
        try:
            bikes = get_filtered_bikes(request.query_params)
            serializer = BikeSerializer(bikes, many=True)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.data, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            new_bike = create_bike(request.data, request.user.id)
            # add charger to user
            if request.accepted_renderer.media_type == 'text/html':
                return Response(DetailedBikeSerializer(new_bike).data, status=status.HTTP_200_OK)
            else:
                return Response(DetailedBikeSerializer(new_bike).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BikesListApiView(APIView, PaginationHandlerMixin):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]
    pagination_class = BasicPagination

    def get(self, request):
        try:
            bikes = get_filtered_bikes(request.query_params)
            page = self.paginate_queryset(bikes)
            if page is not None:
                serializer = BikeListSerializer(page, many=True)
                if request.accepted_renderer.media_type == 'text/html':
                    return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
                else:
                    return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK,
                                    content_type='application/json; charset=utf-8')
            else:
                serializer = BikeListSerializer(bikes, many=True)
                if request.accepted_renderer.media_type == 'text/html':
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.data, status=status.HTTP_200_OK,
                                    content_type='application/json; charset=utf-8')
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)


class DetailedBikeApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

    def get(self, request, bike_id):
        try:
            bike = get_bike_by_id(bike_id)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(DetailedBikeSerializer(bike).data, status=status.HTTP_200_OK)
            else:
                return Response(DetailedBikeSerializer(bike).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        except Bikes.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, bike_id):
        try:
            updated_bike = update_bike(bike_id, request.data, request.user.id)
            if request.accepted_renderer.media_type == 'text/html':
                return Response(DetailedBikeSerializer(updated_bike).data, status=status.HTTP_200_OK)
            else:
                return Response(DetailedBikeSerializer(updated_bike).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        except Bikes.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, bike_id):
        try:
            inactive_bike(bike_id, request.user.id)
            return Response(status=status.HTTP_200_OK)
        except Bikes.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class BikeTypesApiView(APIView):
    authentication_classes = [SessionAuth]
    permission_classes = [IsAuthenticated | Check_API_KEY_Auth]

    def get(self, request):
        try:
            bike_types = get_bikes_type()
            if request.accepted_renderer.media_type == 'text/html':
                return Response(BikeTypeSerializer(bike_types, many=True).data, status=status.HTTP_200_OK)
            else:
                return Response(BikeTypeSerializer(bike_types, many=True).data, status=status.HTTP_200_OK,
                                content_type='application/json; charset=utf-8')
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
