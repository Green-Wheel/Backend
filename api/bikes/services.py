from api.bikes.models import BikeTypes, Bikes
from api.chargers.models import Images
from api.chargers.utils import get_localization, get_town
from utils.imagesS3 import upload_image_to_s3, get_image_from_s3


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
    order = filter_params.get('order', None)
    if order:
        bikes = bikes.order_by(order)
    return bikes


def get_bikes_type():
    return BikeTypes.objects.all()


def create_bike(data, owner_id):
    localization = get_localization(data["latitude"], data["longitude"])
    town = get_town("Barcelona", "Barcelona")
    bike_type = BikeTypes.objects.get(id=data.get("bike_type", 1))
    bike = Bikes(title=data['title'],
                 description=data['description'],
                 direction="Direccio del carrer hardcodejada",
                 town=town,
                 localization=localization,
                 power=data["power"],
                 price=data["price"],
                 bike_type=bike_type,
                 owner_id=owner_id)
    bike.save()
    return bike


def update_bike(bike_id, data, user):
    bike = get_bike_by_id(bike_id)
    if bike.user.id != user.id:
        raise Exception("User not owner of bike")
    localization = get_localization(data["latitude"], data["longitude"])
    town = get_town("Barcelona", "Barcelona")
    bike.name = data.get('name', bike.name)
    bike.description = data.get('description', bike.description)
    bike.price = data.get('price', bike.price)
    bike.power = data.get('power', bike.power)
    bike.bike_type = data.get('bike_type', bike.bike_type)
    bike.localization = localization
    bike.direction = "Direccio del carrer hardcodejada"
    bike.town = town
    # Falta imatges
    bike.save()


def inactive_bike(bike_id):
    bike = get_bike_by_id(bike_id)
    if not bike.active:
        raise Exception("Bike already inactive")
    bike.is_active = False
    bike.save()
    return bike


def upload_images(bike_id, images):
    for file in images.getlist("images"):
        path = "publication/" + str(bike_id) + "/" + file.name
        result = upload_image_to_s3(file, path)
        image = Images(image_path=path, publication_id=bike_id)
        image.save()
        print(result)
    return get_bike_by_id(bike_id)

def get_images(bike_id):
    img = get_image_from_s3('publication/1/foto.png')
    print(img)
