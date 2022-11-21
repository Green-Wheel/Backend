import re

from api.chargers.models import ConnectionsType, SpeedsType, CurrentsType
from api.publications.models import Localizations, Province, Town


def get_speed(speed_name):
    try:
        obj_speed = SpeedsType.objects.filter(name=speed_name)[0]
    except Exception:
        obj_speed = SpeedsType(name=speed_name)
        obj_speed.save()
    return obj_speed


def get_all_speeds(speed):
    all_speeds = []
    if speed is not None:
        speeds = speed.split(" i ")
        for s in speeds:
            all_speeds.append(get_speed(s))
    return all_speeds


def get_connection(connection):
    try:
        obj_connection = ConnectionsType.objects.filter(name=connection)[0]
    except Exception:
        obj_connection = ConnectionsType(name=connection)
        obj_connection.save()
    return obj_connection


def get_all_connections(connection_type):
    all_connections = []
    if connection_type is not None:
        connections = re.split('\+| i ', connection_type)
        for connection in connections:
            connection.replace(",", ".")
            connection = connection.strip().upper()
            all_connections.append(get_connection(connection))
    return all_connections


def get_current(current):
    try:
        obj_current = CurrentsType.objects.filter(name=current)[0]
    except Exception:
        obj_current = CurrentsType(name=current)
        obj_current.save()
    return obj_current


def get_all_currents(current_type):
    all_currents = []
    if current_type is not None:
        currents = current_type.split("-")
        for current in currents:
            all_currents.append(get_current(current))
    return all_currents


def get_localization(latitude, longuitude):
    try:
        obj_localization = Localizations.objects.filter(latitude=latitude, longitude=longuitude)[0]
    except Exception:
        obj_localization = Localizations(latitude=latitude, longitude=longuitude)
        obj_localization.save()
    return obj_localization


def get_town(town_name, province_name):
    try:
        obj_province = Province.objects.filter(name=province_name)[0]
    except Exception:
        obj_province = Province(name=province_name)
        obj_province.save()
    try:
        obj_town = Town.objects.filter(name=town_name, province=obj_province)[0]
    except Exception:
        obj_town = Town(name=town_name, province=obj_province)
        obj_town.save()
    return obj_town
