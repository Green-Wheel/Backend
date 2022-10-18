import requests
import logging

from api.chargers.models import PublicChargers, ConnectionsType, Localizations, Town, Province, SpeedsType, CurrentsType


def get():
    # petició api i actualitzar base de dades
    response = requests.get("https://analisi.transparenciacatalunya.cat/resource/tb2m-m33b.json?")

    return response.json()


def get_public_charger_info(charger):
    agent = charger.get("promotor_gestor")
    identifier = charger.get("ide_pdr")
    access = charger.get("acces")
    return agent, identifier, access


def get_all_speeds(speed):
    speeds = speed.split(" i ")
    all_speeds = []
    for speed in speeds:
        all_speeds.append(SpeedsType.objects.get_or_create(name=speed))
    return all_speeds


def get_all_connections(connection_type):
    connections = connection_type.split("+")
    all_connections = []
    for connection in connections:
        all_connections.append(ConnectionsType.objects.get_or_create(name=connection))
    return all_connections


def get_all_currents(current_type):
    currents = current_type.split("-")
    all_currents = []
    for current in currents:
        all_currents.append(CurrentsType.objects.get_or_create(name=current))
    return all_currents


def get_charger_info(charger):
    power = charger.get("kw")
    speed = charger.get("tipus_velocitat")
    if speed == "FORA DE SERVEI":
        available = False
        speed = None
    else:
        available = True
    all_speeds = get_all_speeds(speed)
    connection_type = charger.get("tipus_connexi")
    all_connections = get_all_connections(connection_type)

    current_type = charger.get("ac_dc")
    all_currents = get_all_currents(current_type)

    return power, all_speeds, available, all_connections, all_currents


def get_publication_info(charger):
    title = None
    description = charger.get("designaci_descriptiva")
    province, created = Province.objects.get_or_create(name=charger.get("provincia"))
    town, created = Town.objects.get_or_create(name=charger.get("municipi"), province_id=province.id)
    localization, created = Localizations.objects.get_or_create(latitude=charger.get("latitud"),
                                                                longitude=charger.get("longitud"),
                                                                direction=charger.get("adre_a"), town_id=town.id)
    print(charger.get("latitud"), charger.get("longitud"), charger.get("adre_a"), town.id)
    print("created: " + str(created))
    return title, description, localization


def filter_localization(charger):
    latitude = charger.get("latitud")
    longitude = charger.get("longitud")
    return PublicChargers.objects.filter(localization__latitude=latitude, localization__longitude=longitude)


def save_chargers_to_db():
    response = get()
    for charger in response:
        public_charger = filter_localization(charger)
        agent, identifier, access = get_public_charger_info(charger)
        power, all_speeds, available, all_connections, all_currents = get_charger_info(charger)
        title, description, localization = get_publication_info(charger)
        if not public_charger.exists():
            public_charger = PublicChargers.objects.create(agent=agent, identifier=identifier,
                                                           access=access, power=power, available=available, title=title,
                                                           description=description, localization=localization)
            print("Public charger created")
            print(public_charger)
        else:
            public_charger.update(agent=agent, identifier=identifier,
                                  access=access, power=power, available=available, title=title,
                                  description=description, localization=localization, speed=all_speeds)
            print(localization.longitude)
            print("Public charger updated")
        public_charger.speed.add(all_speeds)
        # public_charger.speed.set(all_speeds)
        public_charger.connection_type.set(all_connections)
        public_charger.current_type.set(all_currents)
        print("public charger saved")
        print(public_charger)
        public_charger.save()


#if __name__ == '__main__':
    # print(save_chargers_to_db())
