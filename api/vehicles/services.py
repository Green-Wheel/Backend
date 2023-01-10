from datetime import datetime, timedelta
import logging
import requests
from django.core.signals import request_finished

from api.chargers.models import CurrentsType, ConnectionsType, Configs
from api.users.models import Users, Trophies
from api.vehicles.models import CarsModel, CarsBrand, Cars


def __sincronize_data_from_api(signal, **kwargs):
    now_date = datetime.now() - timedelta(hours=1)
    a_day_ago = now_date - timedelta(hours=24)
    try:
        date_obj = Configs.objects.filter(key="vehicles_last_date_checked")[0]
        last_date = datetime.strptime(date_obj.value, "%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        date_obj = Configs(key="vehicles_last_date_checked", value=now_date)
        last_date = datetime(1970, 1, 1)

    if a_day_ago > last_date:
        __get_data_vehicles()
        date_obj.value = now_date
        date_obj.save()


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


def __get_data_vehicles():
    data = __get_data_from_vehicles_api()
    vehicles = []
    if data is not None:
        for vehicle in data["data"]:
            if vehicle["vehicle_type"] == "car":
                vehicles.append(vehicle)
        __parse_model(vehicles)
    print("Finished get data from API")


def set_vehicles_trophies(car_owner_id):
    num_cars = Cars.objects.filter(car_owner_id=car_owner_id).count()
    user = Users.objects.get(id=car_owner_id)
    if num_cars == 1:
        trophie = Trophies.objects.get(id=1)
        user.trophies.add(trophie)
    elif num_cars == 2:
        trophie = Trophies.objects.get(id=2)
        user.trophies.add(trophie)


def create_car(data, car_owner_id):
    car_alias = data["alias"]
    car_license = data["car_license"]
    car_model_id = data["model"]
    charge_capacity = data["charge_capacity"]
    try:
        car = Cars(alias=car_alias, charge_capacity=charge_capacity, car_license=car_license, model_id=car_model_id,
                   car_owner_id=car_owner_id)
        car.save()
        set_vehicles_trophies(car_owner_id)
        return car
    except Exception as e:
        logging.error(e, "Error creating car")
        return None


def get_filtered_vehicles(filter_params, user_id):
    cars = Cars.objects.filter(car_owner=user_id)
    if filter_params.get("orderby") is not None:
        cars = cars.order_by(filter_params.get("orderby"))
    else:
        cars = cars.order_by("id")
    return cars


def get_brands():
    request_finished.connect(__sincronize_data_from_api, dispatch_uid="sincronize_vehicles_data_from_API")
    return CarsBrand.objects.all()


def get_models_by_brand_id(brand_id):
    return CarsModel.objects.filter(car_brand_id=brand_id).distinct("name")


def get_years_of_model(brand_id, model_id):
    model = CarsModel.objects.get(id=model_id)
    return CarsModel.objects.filter(car_brand_id=brand_id, name=model.name).distinct("year")


def get_car_by_id(car_id):
    return Cars.objects.get(id=car_id)


def update_car(car_id, data, user_id):
    car = get_car_by_id(car_id)
    if car.car_owner_id == user_id:
        car.alias = data["alias"]
        car.charge_capacity = data["charge_capacity"]
        car.car_license = data["car_license"]
        car.model_id = data["model"]
        car.save()
        return car
    else:
        raise Exception("You are not the owner of this car")


def delete_car(car_id, user_id):
    car = get_car_by_id(car_id)
    if car.car_owner_id == user_id:
        car.delete()
    else:
        raise Exception("You are not the owner of this car")


def select_car(car_id, user_id):
    car = get_car_by_id(car_id)
    if car.car_owner_id == user_id:
        user = Users.objects.get(id=user_id)
        user.selected_car = car
        user.save()
    else:
        raise Exception("You are not the owner of this car")
