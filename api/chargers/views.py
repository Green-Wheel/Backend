from datetime import datetime, timedelta
from threading import Thread
from time import strptime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import requests_api
from api.chargers.models import PublicChargers, Chargers, PrivateChargers, Localizations, Town, Publication, \
    SpeedsType, CurrentsType, ConnectionsType, configs
from api.chargers.serializers import PublicChargerSerializer, ChargerSerializer, privateChargerSerializer, \
    SpeedTypeSerializer, CurrentTypeSerializer, connectionTypeSerializer
from api.chargers.utils import get_localization, get_speed, get_connection, get_current, get_town


def set_if_not_none(mapping, key, value):
    if value is not None:
        mapping[key] = value


def get_all_parameters_from_url(parameter):
    if parameter is not None:
        parameter_splitted = parameter.split('_')
        values = []
        for p in parameter_splitted:
            values.append(p)
        return values
    else:
        return None


def get_filtered_chargers(request, charger_type):
    filters = {}

    current_type = request.GET.get('current')
    currents = get_all_parameters_from_url(current_type)
    set_if_not_none(filters, 'current_type__name__in', currents)

    speed_type = request.GET.get('speed')
    speeds = get_all_parameters_from_url(speed_type)
    set_if_not_none(filters, 'speed__name__in', speeds)

    connection_type = request.GET.get('connection')
    connections = get_all_parameters_from_url(connection_type)
    set_if_not_none(filters, 'connection_type__name__in', connections)

    if charger_type == "public":
        available = request.GET.get('available')
        set_if_not_none(filters, 'available', available)
        chargers = PublicChargers.objects.filter(**filters)
    elif charger_type == "private":
        price = request.GET.get('price')
        set_if_not_none(filters, 'price__lte', price)
        chargers = PrivateChargers.objects.filter(**filters)
    else:
        chargers = Chargers.objects.filter(**filters)

    return chargers


def sincronize_data_with_API():
    now_date = datetime.now() - timedelta(hours=1)
    try:
        date_obj = Configs.objects.filter(key="last_date_checked")[0]
        last_date = datetime.strptime(date_obj.value, "%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        date_obj = Configs(key="last_date_checked", value=now_date)
        date_obj.save()
        last_date = datetime(1970, 1, 1)

    if now_date > last_date:
        requests_api.save_chargers_to_db()
        date_obj.value = now_date
        date_obj.save()


def get_all_speed(self, speed):
    return map(lambda s: get_speed(s), speed)


def get_all_connection(self, connection):
    return map(lambda c: get_connection(c), connection)


def get_all_current(self, current):
    return map(lambda c: get_current(c), current)


class ChargersView(APIView):
    def get(self, request):
        thread = Thread(target=sincronize_data_with_API)
        thread.start()
        chargers = get_filtered_chargers(request, "all")
        charger_serializer = ChargerSerializer(chargers, many=True)

        return Response(charger_serializer.data, status=status.HTTP_200_OK)


class PublicChargersView(APIView):
    def get(self, request):
        thread = Thread(target=sincronize_data_with_API())
        thread.start()
        chargers = get_filtered_chargers(request, "public")
        charger_serializer = PublicChargerSerializer(chargers, many=True)
        return Response(charger_serializer.data, status=status.HTTP_200_OK)


class PrivateChargerView(APIView):
    def get(self, request):
        try:
            chargers = get_filtered_chargers(request, "private")
            charger_serializer = privateChargerSerializer(chargers, many=True)
            return Response(charger_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        #charger = PrivateChargersSerializer(data=request.data)
        localization = get_localization(request.data["Latitude"], request.data["Longitude"])
        speed_type = get_speed(request.data["speed"])
        connection_type = get_connection(request.data["connection_type"])
        current_type = get_current(request.data["current_type"])
        town = get_town(request.data["town"], "Barcelona")

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
            private_serializer = privateChargerSerializer(private, many=False)

            # add charger to user
            return Response({"res": "Charger added", "data": private_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DetailedPrivateChargerAppView(APIView):
    def get(self, request, charger_id):
        try:
            private = PrivateChargers.objects.get(id=charger_id)
            private_serializer = privateChargerSerializer(private, many=False)
            return Response({"res": "Charger found", "data": private_serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, charger_id):
        localization = get_localization(request.data["Latitude"], request.data["Longitude"])
        speed_type = get_all_speed(request.data["speed"])
        connection_type = get_all_connection(request.data["connection_type"])
        current_type = get_all_current(request.data["current_type"])
        town = get_town(request.data["town"], "Barcelona")

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

            private_serializer = privateChargerSerializer(private, many=False)
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
            return Response({"res": "Error", "message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CurrentTypeView(APIView):
    def get(self, request):
        try:
            currents = CurrentTypeSerializer(CurrentsType.objects.all(), many=True)
            return Response(currents.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error", "message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConnectionTypeView(APIView):
    def get(self, request):
        try:
            connections = connectionTypeSerializer(ConnectionsType.objects.all(), many=True)
            return Response(connections.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"res": "Error", "message": e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
