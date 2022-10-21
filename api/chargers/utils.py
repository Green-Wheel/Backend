from django.db import IntegrityError
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors

from api.chargers.models import PublicChargers, ConnectionsType, Localizations, Town, Province, SpeedsType, CurrentsType


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