from api.publications.models import Images, Publication
from utils.imagesS3 import upload_image_to_s3
from calendar import monthrange
from datetime import time

from api.bikes.models import Bikes
from api.bikes.serializers import DetailedBikeSerializer, BikeListSerializer
from api.bookings.serializers import SimpleBookingsSerializer
from api.chargers.models import Chargers, PrivateChargers, PublicChargers
from api.chargers.serializers import DetailedChargerSerializer, ChargerListSerializer
from api.publications.models import Publication, OccupationRangesType, OccupationRepeatMode, OccupationRanges
from api.publications.serializers import OccupationRangeSerializer

def create_booking_occupation(data,publication_id):
    if PublicChargers.objects.filter(id=publication_id).count() > 0:
        raise Exception("You can't create an occupation for a public charger")
    data["related_publication"] = publication_id
    data["occupation_range_type"] = 1
    data["repeat_mode"] = 1
    serializer = OccupationRangeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.errors)
def create_occupation(data, user_id, publication_id):
    publication = Publication.objects.get(id=publication_id)
    if publication.owner.id != user_id:
        raise Exception("You are not the owner of the publication")
    if PublicChargers.objects.filter(id=publication_id).count() > 0:
        raise Exception("You can't create an occupation for a public charger")
    ranges = []
    r = {}
    for range in data["ranges"]:
        r["related_publication"] = publication_id
        r["occupation_range_type"] = 2
        r["repeat_mode"] = range.get("repeatmode", 1)
        r["start_date"] = range.get("start_date", None)
        r["end_date"] = range.get("end_date", None)
        r["booking_id"] = None
        serializer = OccupationRangeSerializer(data=r)
        if serializer.is_valid():
            serializer.save()
            ranges.append(serializer.data)
        else:
            raise Exception(serializer.errors)
    return ranges


def get_ocupation_by_id(ocupation_id):
    return OccupationRanges.objects.get(id=ocupation_id)


def update_occupation(ocupation_id, data, user_id):
    occupation = get_ocupation_by_id(ocupation_id)
    if occupation.related_publication.owner.id != user_id:
        raise Exception("You are not the owner of the publication")
    data["related_publication"] = occupation.related_publication.id
    data["occupation_range_type"] = data.get("occupation_type", 2)
    data["repeat_mode"] = data.get("repeatmode", 1)
    serializer = OccupationRangeSerializer(occupation, data=data)
    if serializer.is_valid():
        serializer.save()
        return get_ocupation_by_id(ocupation_id)
    else:
        raise Exception(serializer.errors)


def delete_occupation(ocupation_id, user_id):
    occupation = get_ocupation_by_id(ocupation_id)
    if occupation.related_publication.owner.id != user_id:
        raise Exception("You are not the owner of the publication")
    occupation.delete()

def get_occupation_by_month(publication_id, year, month,day):
    occupations = OccupationRanges.objects.filter(related_publication=publication_id, start_date__year=year,
                                                  start_date__month=month,start_date__day=day)
    start_day_time = time(0, 0, 0)
    end_day_time = time(23, 59, 59)
    if day is None:
        days = {}
    else:
        days = []
    for occupation in occupations:
        for i in range(occupation.start_date.day, occupation.end_date.day + 1):
            occupation_strip = {}
            if i not in days and day is None:
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
                occupation_strip["booking"] = SimpleBookingsSerializer(occupation.booking).data
            if day is None:
                days[i].append(occupation_strip)
            else:
                days.append(occupation_strip)
    return days

def get_publication_by_id(publication_id):
    return Publication.objects.get(id=publication_id)


def upload_images(publication_id, images, user_id):
    print("upload_images")
    publication = get_publication_by_id(publication_id)
    owner = publication.owner
    if owner.id != user_id:
        raise Exception("User is not the owner of this publication")
    for file in images:
        path = "publication/" + str(publication_id) + "/" + file.name
        s3_path = upload_image_to_s3(file, path)
        image = Images(image_path=s3_path, publication_id=publication_id)
        image.save()
    return publication


def get_repeat_types():
    return OccupationRepeatMode.objects.all()