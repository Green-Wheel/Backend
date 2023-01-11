from django.core.signals import request_finished

from api.bikes.models import BikeTypes, Bikes
from api.chargers.utils import get_localization, get_town
from api.publications.services import get_contamination, sincronize_data_with_API_contamination
from api.users.models import Users, Trophies
from utils.nearby_publications import get_nearby_publications


def __get_filter(filter_params):
    filters = {}
    if filter_params.get('town'):
        filters['town__id'] = filter_params['town']
    if filter_params.get('bike_type'):
        filters['bike_type__id'] = filter_params['bike_type']
    if filter_params.get('price'):
        filters['price__lte'] = filter_params['price']
    if filter_params.get('power'):
        filters['power__gte'] = filter_params['power']
    return filters


def get_all_bikes():
    return Bikes.objects.all()


def get_bike_by_id(id):
    return Bikes.objects.get(id=id)


def get_filtered_bikes(filter_params):
    filters = __get_filter(filter_params)
    filters['active'] = True
    bikes = Bikes.objects.filter(**filters)
    bikes = get_nearby_publications(bikes, filter_params)
    order = filter_params.get('order', None)
    if order and order != "distance":
        bikes = bikes.order_by(order)
    elif order is None:
        bikes = bikes.order_by('id')

    request_finished.connect(sincronize_data_with_API_contamination,
                             dispatch_uid="sincronize_data_with_API_contamination")
    return bikes


def get_bikes_type():
    return BikeTypes.objects.all()


def set_bikes_trophies(owner_id):
    owner = Users.objects.get(id=owner_id)
    num_chargers = Bikes.objects.filter(owner_id=owner_id).count()
    if num_chargers == 1:
        trophy = Trophies.objects.get(id=3)
        owner.trophies.add(trophy)
    elif num_chargers == 2:
        trophy = Trophies.objects.get(id=4)
        owner.trophies.add(trophy)
    owner.level = owner.trophies.count()
    owner.save()


def create_bike(data, owner_id):
    localization = get_localization(data["latitude"], data["longitude"])
    town = get_town("Barcelona", "Barcelona")
    bike_type = BikeTypes.objects.get(id=data.get("bike_type", 1))
    contamination = get_contamination(data["latitude"], data["longitude"])
    bike = Bikes(title=data['title'], description=data['description'], direction=data['direction'], town=town,
                 localization=localization, power=data["power"], price=data["price"], bike_type=bike_type,
                 owner_id=owner_id, contamination=contamination)
    bike.save()
    set_bikes_trophies(owner_id)
    return bike


def update_bike(bike_id, data, user):
    bike = get_bike_by_id(bike_id)
    if bike.owner.id != user:
        raise Exception("User not owner of bike")
    localization = get_localization(data["latitude"], data["longitude"])
    town = get_town(data["town"], data["province"])
    bike.title = data.get('title', bike.title)
    bike.description = data.get('description', bike.description)
    bike.price = data.get('price', bike.price)
    bike.power = data.get('power', bike.power)
    bike.bike_type.id = data.get('bike_type', bike.bike_type.id)
    bike.localization = localization
    bike.direction = "Direccio del carrer hardcodejada"
    bike.town = town
    # Falta imatges
    bike.save()
    return bike


def inactive_bike(bike_id, user):
    bike = get_bike_by_id(bike_id)
    if bike.owner.id != user:
        raise Exception("User not owner of bike")
    if not bike.active:
        raise Exception("Bike already inactive")
    bike.is_active = False
    bike.save()
