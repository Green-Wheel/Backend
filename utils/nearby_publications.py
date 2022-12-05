from django.db.models import F
from django.db.models.functions import Radians, Cos, Power, Sin, ATan2, Sqrt


def get_nearby_publications(publications,filter_params):
    # https://stackoverflow.com/questions/1185408/converting-from-longitude-latitude-to-cartesian-coordinates
    # https://stackoverflow.com/questions/120283/working-with-latitude-longitude-values-in-python
    try:
        longitude = float(filter_params.get("longitude"))
        latitude = float(filter_params.get("latitude"))
        radius = filter_params.get("radius")
        zoom = filter_params.get("zoom")
        if radius is None and zoom is not None:
            radius = 1000 * 2 ** (18 - int(zoom))
        radius = float(radius)
        # convert to radians
        dlat = Radians(F('localization__latitude') - latitude)
        dlong = Radians(F('localization__longitude') - longitude)

        a = (Power(Sin(dlat / 2), 2) + Cos(Radians(latitude))
             * Cos(Radians(F('localization__latitude'))) * Power(Sin(dlong / 2), 2)
             )

        c = 2 * ATan2(Sqrt(a), Sqrt(1 - a))
        d = 6371 * c

        # filter by distance
        publications = publications.annotate(distance=d).filter(distance__lte=radius)
        if filter_params.get("order") == "distance":
            publications = publications.order_by("distance")
        return publications
    except Exception as e:
        return publications