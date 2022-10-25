from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import requests_api
from api.chargers.models import PublicChargers, Chargers, PrivateChargers, Localizations, Town, Publication, \
    SpeedsType, CurrentsType
from api.chargers.serializers import PublicChargerSerializer, ChargerSerializer, privateChargerSerializer, \
    PublicationSerializer, SpeedTypeSerializer, CurrentTypeSerializer, connectionTypeSerializer
from api.chargers.utils import get_localization, get_speed, get_connection, get_current, get_town

class ChargersView(APIView):
    def set_if_not_none(self, mapping, key, value):
        if value is not None:
            mapping[key] = value

    def get(self, request):
        # Agafar de la base de dades

        filters = {}
        charger_type = request.GET.get('charger_type')
        # town = request.GET.get('town')
        # self.set_if_not_none(filters, 'town', town)
        # self.set_if_not_none(filters, 'speed', speed)
        self.set_if_not_none(filters, 'charger_type', charger_type)

        if charger_type == "public":
            chargers = PublicChargers.objects.filter(**filters)
        elif charger_type == "private":
            chargers = PrivateChargers.objects.filter(**filters)
        else:
            chargers = Chargers.objects.filter(**filters)

        charger_serializer = PublicChargerSerializer(chargers, many=True)
        requests_api.save_chargers_to_db()
        # create threat: save_chargers_to_db(), dins d'aqui hi haura la comprovacio si s'ha d'actualitzar o no a bd (si la data ultima posada es de fa mes de 1 hora) --> puc posaru fora
        return Response(charger_serializer.data, status=status.HTTP_200_OK)


def get_all_speed(self, speed):
    return map(lambda s: get_speed(s), speed)

def get_all_connection(self, connection):
    return map(lambda c: get_connection(c), connection)

def get_all_current(self, current):
    return map(lambda c: get_current(c), current)

class PrivateChargerView(APIView):
    def post(self, request):
        localization = get_localization(request.data["Latitude"], request.data["Longitude"])
        speed_type = get_speed(request.data["velocity"])
        connection_type = get_connection(request.data["tipusCarregador"])
        current_type = get_current(request.data["current"])
        town = get_town("Barcelona", "Barcelona")

        try:
            private = PrivateChargers(title=request.data['title'],
                                      description=request.data['description'],
                                      direction=request.data['direction'],
                                      town=town,
                                      localization=localization,
                                      power=request.data["power"],
                                      price=request.data["price"])
            private.save()
            private.speed.set([speed_type])
            private.connection_type.set([connection_type])
            private.current_type.set([current_type])
            private_serializaer = privateChargerSerializer(private, many=False)

            #add charger to user


            return Response({"res": "Charger added", "data":private_serializaer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DetailedPrivateChargerAppView(APIView):
    def get(selfself, request, charger_id):
        try:
            private = PrivateChargers.objects.get(id=charger_id)
            private_serializaer = privateChargerSerializer(private, many=False)
            return Response({"res": "Charger found", "data": private_serializaer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self, request,  charger_id):
        localization = get_localization(request.data["Latitude"], request.data["Longitude"])
        speed_type = get_all_speed(request.data["velocity"])
        connection_type = get_all_connection(request.data["tipusCarregador"])
        current_type = get_all_current(request.data["current"])
        town = get_town("Barcelona", "Barcelona")

        try:
            private = PrivateChargers.objects.get(id=charger_id)

            private.title = request.data["title"]
            private.description = request.data["description"]
            private.direction = request.data["direction"]
            private.power = request.data["power"]
            private.price = request.data["price"]
            private.localization = localization
            private.speed.set(speed_type)
            private.connection_type.set(connection_type)
            private.current_type.set(current_type)

            private_serializaer = privateChargerSerializer(private, many=False)
            return Response({"res": "Charger edited"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, charger_id):
        try:
            private = PrivateChargers.objects.get(id=charger_id)
            private.delete()
            return Response({"res": "Charger deleted"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SpeedTypeView(APIView):
    def get(self, request):
        try:
            speeds = SpeedTypeSerializer(SpeedsType.objects.all(), many=True)
            return Response(speeds.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error", "message":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CurrentTypeView(APIView):
    def get(self, request):
        try:
            currents = CurrentTypeSerializer(CurrentsType.objects.all(), many=True)
            return Response(currents.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error", "message":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConnectionTypeView(APIView):
    def get(self, request):
        try:
            connections = connectionTypeSerializer(ConnectionsType.objects.all(), many=True)
            return Response(connections.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error", "message":e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)