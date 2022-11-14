from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.chargers.models import Chargers

from .services import get_filtered_chargers, create_private_charger, get_charger_by_id, update_private_charger, \
    delete_private_charger, get_speeds, get_connections, get_currents
from ..users.permissions import Check_API_KEY_Auth


class ChargersView(APIView):
    permission_classes = [Check_API_KEY_Auth]

    def get(self, request):
        chargers = get_filtered_chargers(request.query_params)
        return Response(chargers, status=status.HTTP_200_OK)


class DetailedChargerView(APIView):
    permission_classes = [Check_API_KEY_Auth]

    def get(self, request, id):
        try:
            charger = get_charger_by_id(id)
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
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DetailedPrivateChargerAppView(APIView):
    def put(self, request, id):
        try:
            private_charger = update_private_charger(id, request.data)
            return Response(private_charger, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, charger_id):
        try:
            delete_private_charger(charger_id)
            return Response({"res": "Charger deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SpeedTypeView(APIView):
    def get(self, request):
        try:
            speeds = get_speeds()
            return Response(speeds, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CurrentTypeView(APIView):
    def get(self, request):
        try:
            currents = get_currents()
            return Response(currents, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConnectionTypeView(APIView):
    def get(self, request):
        try:
            connections = get_connections()
            return Response(connections, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
