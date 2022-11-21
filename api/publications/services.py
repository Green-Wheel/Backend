from calendar import monthrange
from datetime import time

from api.bikes.models import Bikes
from api.bikes.serializers import DetailedBikeSerializer, BikeListSerializer
from api.chargers.models import Chargers, PrivateChargers, PublicChargers
from api.chargers.serializers import DetailedChargerSerializer, ChargerListSerializer
from api.publications.models import Publication, OccupationRangesType, OccupationRepeatMode, OccupationRanges
from api.publications.serializers import OccupationRangeSerializer


def create_occupation(data, user_id, publication_id):
    publication = Publication.objects.get(id=publication_id)
    if publication.owner.id != user_id:
        raise Exception("You are not the owner of the publication")
    if PublicChargers.objects.filter(id=publication_id).count() > 0:
        raise Exception("You can't create an occupation for a public charger")
    data["related_publication"] = publication_id
    data["occupation_range_type"] = 2
    data["repeat_mode"] = data.get("repeatmode", 1)
    serializer = OccupationRangeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return OccupationRanges.objects.latest('id')
    else:
        raise Exception(serializer.errors)


def get_ocupation_by_id(ocupation_id):
    return OccupationRanges.objects.get(id=ocupation_id)



def update_occupation(ocupation_id, data,user_id):
    occupation = get_ocupation_by_id(ocupation_id)
    if occupation.related_publication.owner.id != user_id:
        raise Exception("You are not the owner of the publication")
    data["related_publication"] = occupation.related_publication.id
    data["occupation_range_type"] = 2
    data["repeat_mode"] = data.get("repeatmode", 1)
    serializer = OccupationRangeSerializer(occupation, data=data)
    if serializer.is_valid():
        serializer.save()
        return get_ocupation_by_id(ocupation_id)
    else:
        raise Exception(serializer.errors)


def delete_occupation(ocupation_id,user_id):
    occupation = get_ocupation_by_id(ocupation_id)
    if occupation.related_publication.owner.id != user_id:
        raise Exception("You are not the owner of the publication")
    occupation.delete()



def get_occupation_by_month(publication_id, year,month):
    occupations = OccupationRanges.objects.filter(related_publication=publication_id, start_date__month=month)
    start_day_time = time(0, 0, 0)
    end_day_time = time(23, 59, 59)
    days = {}
    for occupation in occupations:
        for i in range(occupation.start_date.day, occupation.end_date.day + 1):
            occupation_strip = {}
            if i not in days:
                days[i] = []
            if occupation.start_date.day == i:
                occupation_strip["start_time"] = occupation.start_date.time()
            else:
                occupation_strip["start_time"] = start_day_time
            if occupation.end_date.day == i:
                occupation_strip["end_time"] = occupation.end_date.time()
            else:
                occupation_strip["end_time"] = end_day_time
            occupation_strip["id"] = occupation.id
            occupation_strip["occupation_range_type"] = occupation.occupation_range_type.id
            if occupation_strip["occupation_range_type"] == 1:
                occupation_strip["booking"] = occupation.booking.id
            days[i].append(occupation_strip)

    return days
