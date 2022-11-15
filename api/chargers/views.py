from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from api.chargers.models import Chargers
from .pagination import PaginationHandlerMixin
from .serializers import ChargerSerializer

from .services import get_filtered_chargers, create_private_charger, get_charger_by_id, update_private_charger, \
    delete_private_charger, get_speeds, get_connections, get_currents
from ..users.permissions import Check_API_KEY_Auth

class BasicPagination(PageNumberPagination):
    page_size_query_param = 'limit'

class ChargersView(APIView,PaginationHandlerMixin):
    permission_classes = [Check_API_KEY_Auth]
    pagination_class = BasicPagination

    def get(self, request):
        try:
            chargers = get_filtered_chargers(request.query_params)
            page = self.paginate_queryset(chargers)
            if page is not None:
                serializer = ChargerSerializer(page, many=True)
                return Response(self.get_paginated_response(serializer.data).data, status=status.HTTP_200_OK)
            else:
                serializer = ChargerSerializer(chargers, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)


class DetailedChargerView(APIView):
    permission_classes = [Check_API_KEY_Auth]

    def get(self, request, charger_id):
        try:
            charger = get_charger_by_id(charger_id)
            return Response(charger, status=status.HTTP_200_OK)
        except Chargers.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PrivateChargersView(APIView):
    permission_classes = [Check_API_KEY_Auth]

    def post(self, request):
        try:
            new_private_charger = create_private_charger(request.data)
            # add charger to user
            return Response({new_private_charger}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DetailedPrivateChargerAppView(APIView):
    def put(self, request, id):
        try:
            private_charger = update_private_charger(id, request.data)
            return Response(private_charger, status=status.HTTP_200_OK)
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
            return Response(speeds, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_404_NOT_FOUND)


class CurrentTypeView(APIView):
    def get(self, request):
        try:
            currents = get_currents()
            return Response(currents, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_404_NOT_FOUND)


class ConnectionTypeView(APIView):
    def get(self, request):
        try:
            connections = get_connections()
            return Response(connections, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_404_NOT_FOUND)
