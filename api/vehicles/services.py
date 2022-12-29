import datetime
import logging
import requests

from api.chargers.models import CurrentsType, ConnectionsType
from api.vehicles.models import CarsModel, CarsBrand, Cars


def __get_data_from_vehicles_api():
    response = requests.get("https://raw.githubusercontent.com/chargeprice/open-ev-data/master/data/ev-data.json")
    if response.status_code == 200:
        return response.json()
    else:
        logging.error("Error getting data from API")
        return None


def __parse_brand(brand):
    try:
        obj_brand = CarsBrand.objects.get(name=brand)
    except Exception as e:
        obj_brand = CarsBrand(name=brand)
        obj_brand.save()
    return obj_brand


def __parse_chargers_type(v):
    currents = []
    connections = []
    if v["ac_charger"] is not None:
        current = CurrentsType.objects.filter(name="AC")[0]
        currents.append(current)
        ports = v["ac_charger"]["ports"]
        for port in ports:
            if port == "type1":
                connection = ConnectionsType.objects.filter(name="SCHUKO")[0]
                connections.append(connection)
            elif port == "type2":
                connection = ConnectionsType.objects.filter(name="MENNEKES")[0]
                connections.append(connection)
    if v["dc_charger"] is not None:
        current = CurrentsType.objects.filter(name="DC")[0]
        currents.append(current)
        ports = v["dc_charger"]["ports"]
        for port in ports:
            if port == "tesla_suc" or port == "tesla_ccs":
                connection = ConnectionsType.objects.filter(name="TESLA")[0]
                connections.append(connection)
            else:
                connection = ConnectionsType.objects.filter(name=port.upper())[0]
                connections.append(connection)
    return currents, connections


def __parse_model(vehicles):
    for v in vehicles:
        name = v["model"]
        obj_brand = __parse_brand(v["brand"])
        year = v["release_year"]
        autonomy = v["usable_battery_size"]
        currents, connections = __parse_chargers_type(v)
        consumption = v["energy_consumption"]["average_consumption"]

        try:
            if v["release_year"] is not None:
                obj_model = CarsModel.objects.filter(name=name, year=year, car_brand=obj_brand)[0]
            else:
                obj_model = CarsModel.objects.filter(name=name, car_brand=obj_brand)[0]
        except Exception as e:
            obj_model = CarsModel(name=name, year=year, autonomy=autonomy, car_brand=obj_brand, consumption=consumption)
            obj_model.save()

        if len(currents) > 0:
            obj_model.current_type.set(currents)
            obj_model.save()
        if len(connections) > 0:
            obj_model.connection_type.set(connections)
            obj_model.save()


def get_data_vehicles():
    data = __get_data_from_vehicles_api()
    vehicles = []
    if data is not None:
        for vehicle in data["data"]:
            if vehicle["vehicle_type"] == "car":
                vehicles.append(vehicle)
        __parse_model(vehicles)
    print("Finished get data from API")


def create_car(data, car_owner_id):
    car_license = data["car_license"]
    car_model_id = data["model"]
    charge_capacity = data["charge_capacity"]
    try:
        car = Cars(charge_capacity=charge_capacity, car_license=car_license, model_id=car_model_id, car_owner_id=1)
        car.save()
        return car
    except Exception as e:
        logging.error(e, "Error creating car")
        return None
