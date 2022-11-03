import requests
import logging

from api.chargers.models import PublicChargers, Localizations, Town, Province
from api.chargers.utils import get_all_speeds, get_all_connections, get_all_currents


def get():
    # petició api i actualitzar base de dades
    response = requests.get("https://analisi.transparenciacatalunya.cat/resource/tb2m-m33b.json?")
    if response.status_code == 200:
        return response.json()
    else:
        logging.error("Error getting data from API")
        return None


def get_charger_info(c_speed, c_connection, c_current):
    if c_speed == "FORA DE SERVEI":
        available = False
        c_speed = None
    else:
        available = True
    all_speeds = get_all_speeds(c_speed)
    all_connections = get_all_connections(c_connection)
    all_currents = get_all_currents(c_current)
    return all_speeds, available, all_connections, all_currents


def get_publication_info(c_province, c_town, c_latitude, c_longitude):
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


def filter_localization(c_latitude, c_longitude, c_direction):
    try:
        obj_pc = PublicChargers.objects.filter(localization__latitude=c_latitude, localization__longitude=c_longitude,
                                               direction=c_direction)[0]
    except Exception:
        obj_pc = None
    return obj_pc


def create_charger(agent, identifier, access, power, all_speeds, available, all_connections,
                   all_currents, title, description, direction, town, localization):
    public_charger = filter_localization(localization.latitude, localization.longitude, direction)

    if public_charger is None:
        public_charger = PublicChargers(agent=agent, identifier=identifier, access=access, power=power,
                                        available=available, title=title, description=description,
                                        localization=localization, town=town, direction=direction)
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


def save_chargers_to_db():
    print("Getting data from API")
    response = get()
    for charger in response:
        agent, identifier, access, power = charger.get("agent"), charger.get("ide_pdr"), charger.get("access"), charger.get("kw")
        all_speeds, available, all_connections, all_currents = get_charger_info(charger.get("tipus_velocitat"), charger.get("tipus_connexi"), charger.get("ac_dc"))
        title, description, direction = None, charger.get("designaci_descriptiva"), charger.get("adre_a")
        town, localization = get_publication_info(charger.get("provincia"), charger.get("municipi"), charger.get("latitud"), charger.get("longitud"))
        create_charger(agent, identifier, access, power, all_speeds, available, all_connections, all_currents, title, description, direction, town, localization)

    print("Finished  get data from API")
