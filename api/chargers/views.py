from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from api.chargers.models import Chargers
from utils import BasicPagination
from .pagination import PaginationHandlerMixin
from .serializers import ChargerSerializer, DetailedChargerSerializer, SpeedTypeSerializer, CurrentTypeSerializer, \
    ConnectionTypeSerializer, ChargerListSerializer

from .services import get_filtered_chargers, create_private_charger, get_charger_by_id, update_private_charger, \
    delete_private_charger, get_speeds, get_connections, get_currents
from ..users.permissions import Check_API_KEY_Auth





class ChargersView(APIView, PaginationHandlerMixin):
    permission_classes = [Check_API_KEY_Auth]

    def get(self, request):
        try:
            chargers = get_filtered_chargers(request.query_params)

            serializer = ChargerSerializer(chargers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)},status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            new_private_charger = create_private_charger(request.data, request.user.id)
            # add charger to user
            return Response(DetailedChargerSerializer(new_private_charger).data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ChargersListView(APIView, PaginationHandlerMixin):
    permission_classes = [Check_API_KEY_Auth]
    pagination_class = BasicPagination

    def get(self, request):
        try:
            chargers = get_filtered_chargers(request.query_params)
            page = self.paginate_queryset(chargers)
            if page is not None:
                serializer = ChargerListSerializer(page, many=True)
                return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
            else:
                serializer = ChargerListSerializer(chargers, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DetailedChargerView(APIView):
    permission_classes = [Check_API_KEY_Auth]

    def get(self, request, charger_id):
        try:
            charger = get_charger_by_id(charger_id)
            return Response(DetailedChargerSerializer(charger).data, status=status.HTTP_200_OK)
        except Chargers.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, charger_id):
        try:
            private_charger = update_private_charger(charger_id, request.data)
            return Response(DetailedChargerSerializer(private_charger).data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, charger_id):
        try:
            delete_private_charger(charger_id)
            return Response({"res": "Charger deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_404_NOT_FOUND)


class SpeedTypeView(APIView):
    def get(self, request):
        try:
            speeds = get_speeds()
            return Response(SpeedTypeSerializer(speeds, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_404_NOT_FOUND)


class CurrentTypeView(APIView):
    def get(self, request):
        try:
            currents = get_currents()
            return Response(CurrentTypeSerializer(currents, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_404_NOT_FOUND)


class ConnectionTypeView(APIView):
    def get(self, request):
        try:
            connections = get_connections()
            return Response(ConnectionTypeSerializer(connections, many=True).data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_404_NOT_FOUND)
