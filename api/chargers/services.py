from datetime import datetime, timedelta

from django.core.signals import request_finished

from api.chargers.models import Chargers, PrivateChargers, Configs, SpeedsType, ConnectionsType, CurrentsType
import requests
import logging

from api.chargers.models import PublicChargers, Localizations, Town, Province
from api.chargers.serializers import ChargerSerializer, PublicChargerSerializer, PrivateChargerSerializer, \
    SpeedTypeSerializer, CurrentTypeSerializer, ConnectionTypeSerializer, DetailedChargerSerializer, \
    FullPrivateChargerSerializer
from api.chargers.utils import get_all_speeds, get_all_connections, get_all_currents, get_speed, get_connection, \
    get_current, get_localization, get_town


def __sincronize_data_with_API(signal, **kwargs):
    now_date = datetime.now() - timedelta(hours=1)
    an_hour_ago = now_date - timedelta(hours=1)
    try:
        date_obj = Configs.objects.filter(key="last_date_checked")[0]
        last_date = datetime.strptime(date_obj.value, "%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        date_obj = Configs(key="last_date_checked", value=now_date)
        date_obj.save()
        last_date = datetime(1970, 1, 1)

    if an_hour_ago > last_date:
        __save_chargers_to_db()
        date_obj.value = now_date
        date_obj.save()


def __set_if_not_none(mapping, key, value):
    if value is not None:
        mapping[key] = value


def __get_all_parameters_from_url(parameter):
    if parameter is not None:
        parameter_splitted = parameter.split('_')
        values = []
        for p in parameter_splitted:
            values.append(p)
        return values
    else:
        return None


def __get_filter(query_params):
    filters = {}

    current_type = query_params.get('current')
    currents = __get_all_parameters_from_url(current_type)
    __set_if_not_none(filters, 'current_type__name__in', currents)

    speed_type = query_params.get('speed')
    speeds = __get_all_parameters_from_url(speed_type)
    __set_if_not_none(filters, 'speed__name__in', speeds)

    connection_type = query_params.get('connection')
    connections = __get_all_parameters_from_url(connection_type)
    __set_if_not_none(filters, 'connection_type__name__in', connections)

    charger_type = query_params.get('type')
    if charger_type == "public":
        available = query_params.get('available')
        __set_if_not_none(filters, 'available', available)
    elif charger_type == "private":
        price = query_params.get('price')
        __set_if_not_none(filters, 'price__lte', price)

    return filters, charger_type


def __get_data_from_chargers_api():
    # petició api i actualitzar base de dades
    response = requests.get("https://analisi.transparenciacatalunya.cat/resource/tb2m-m33b.json?")
    if response.status_code == 200:
        return response.json()
    else:
        logging.error("Error getting data from API")
        return None


def __get_charger_info(c_speed, c_connection, c_current):
    if c_speed == "FORA DE SERVEI":
        available = False
        c_speed = None
    else:
        available = True
    all_speeds = get_all_speeds(c_speed)
    all_connections = get_all_connections(c_connection)
    all_currents = get_all_currents(c_current)
    return all_speeds, available, all_connections, all_currents


def __get_publication_info(c_province, c_town, c_latitude, c_longitude):
    try:
        obj_province = Province.objects.filter(name=c_province)[0]
    except Exception:
        obj_province = Province(name=c_province)
        obj_province.save()

    try:
        obj_town = Town.objects.filter(name=c_town, province_id=obj_province.id)[0]
    except Exception:
        obj_town = Town(name=c_town, province_id=obj_province.id)
        obj_town.save()

    try:
        obj_localization = Localizations.objects.filter(latitude=c_latitude, longitude=c_longitude)[0]
    except Exception:
        obj_localization = Localizations(latitude=c_latitude, longitude=c_longitude)
        obj_localization.save()

    return obj_town, obj_localization


def __filter_localization(c_latitude, c_longitude, c_direction):
    try:
        obj_pc = PublicChargers.objects.filter(localization__latitude=c_latitude, localization__longitude=c_longitude,
                                               direction=c_direction)[0]
    except Exception:
        obj_pc = None
    return obj_pc


def __create_public_charger(agent, identifier, access, power, all_speeds, available, all_connections,
                            all_currents, title, description, direction, town, localization):
    public_charger = __filter_localization(localization.latitude, localization.longitude, direction)

    if public_charger is None:
        public_charger = PublicChargers(agent=agent, identifier=identifier, access=access, power=power,
                                        available=available, title=title, description=description,
                                        localization=localization, town=town, direction=direction, owner=None)
    else:
        public_charger.agent = agent
        public_charger.identifier = identifier
        public_charger.access = access
        public_charger.power = power
        public_charger.available = available
        public_charger.title = title
        public_charger.description = description
        public_charger.localization = localization
        public_charger.town = town
        public_charger.direction = direction

    public_charger.save()

    if len(all_speeds) > 0:
        public_charger.speed.set(all_speeds)
    if len(all_connections) > 0:
        public_charger.connection_type.set(all_connections)
    if len(all_currents) > 0:
        public_charger.current_type.set(all_currents)

    public_charger.save()


def __save_chargers_to_db():
    print("Getting data from API")
    response = __get_data_from_chargers_api()
    for charger in response:
        agent, identifier, access, power = charger.get("agent"), charger.get("ide_pdr"), charger.get(
            "access"), charger.get("kw")
        all_speeds, available, all_connections, all_currents = __get_charger_info(charger.get("tipus_velocitat"),
                                                                                  charger.get("tipus_connexi"),
                                                                                  charger.get("ac_dc"))
        title, description, direction = None, charger.get("designaci_descriptiva"), charger.get("adre_a")
        town, localization = __get_publication_info(charger.get("provincia"), charger.get("municipi"),
                                                    charger.get("latitud"), charger.get("longitud"))
        __create_public_charger(agent, identifier, access, power, all_speeds, available, all_connections, all_currents,
                                title, description, direction, town, localization)

    print("Finished  get data from API")


def get_all_chargers():
    return ChargerSerializer(Chargers.objects.all(), many=True).data


def get_filtered_chargers(filter_params):
    filters, charger_type = __get_filter(filter_params)
    if charger_type == "public":
        chargers = PublicChargers.objects.filter(**filters)
    elif charger_type == "private":
        chargers = PrivateChargers.objects.filter(**filters)
    else:
        chargers = Chargers.objects.filter(**filters)
    request_finished.connect(__sincronize_data_with_API, dispatch_uid="sincronize_data_with_API")
    return chargers


def get_charger_by_id(charge_id):
    return DetailedChargerSerializer(Chargers.objects.get(id=charge_id), many=False).data


def create_private_charger(data):
    localization = get_localization(data["Latitude"], data["Longitude"])
    speed_type = get_speed(data["speed"])
    connection_type = get_connection(data["connection_type"])
    current_type = get_current(data["current_type"])
    town = get_town(data["town"], "Barcelona")

    private = PrivateChargers(title=data['title'],
                              description=data['description'],
                              direction=data['direction'],
                              town=town,
                              localization=localization,
                              power=data["power"],
                              price=data["price"])
    private.save()
    private.speed.set([speed_type])
    private.connection_type.set([connection_type])
    private.current_type.set([current_type])
    return FullPrivateChargerSerializer(private).data


def update_private_charger(id, data):
    localization = get_localization(data["Latitude"], data["Longitude"])
    speed_type = get_all_speeds(data["speed"])
    connection_type = get_all_connections(data["connection_type"])
    current_type = get_all_currents(data["current_type"])
    town = get_town(data["town"], "Barcelona")

    private = PrivateChargers.objects.get(id=id)

    private.title = data["title"]
    private.description = data["description"]
    private.direction = data["direction"]
    private.power = data["power"]
    private.price = data["price"]
    private.town = town
    private.localization = localization
    private.speed.set(speed_type)
    private.connection_type.set(connection_type)
    private.current_type.set(current_type)

    return PrivateChargerSerializer(private).data


def delete_private_charger(id):
    private = PrivateChargers.objects.get(id=id)
    private.delete()


def get_speeds():
    return SpeedTypeSerializer(SpeedsType.objects.all(), many=True).data


def get_connections():
    return ConnectionTypeSerializer(ConnectionsType.objects.all(), many=True).data


def get_currents():
    return CurrentTypeSerializer(CurrentsType.objects.all(), many=True).data
