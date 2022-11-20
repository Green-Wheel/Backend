from api.bikes.models import BikeTypes, Bikes


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
    bikes = Bikes.objects.filter(**filters)
    order = filter_params.get('order', None)
    if order:
        bikes = bikes.order_by(order)
    return bikes


def get_bikes_type():
    return BikeTypes.objects.all()

def create_bike(data, user):
    pass

def update_bike(bike_id, data, user):
    pass

def inactive_bike(bike_id):
    pass
