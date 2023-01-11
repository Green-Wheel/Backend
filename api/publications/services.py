from api.publications.models import Images, Contamination
from utils.imagesS3 import upload_image_to_s3
from datetime import time, datetime, timedelta
import requests

from api.bookings.serializers import SimpleBookingsSerializer
from api.chargers.models import PublicChargers, Configs
from api.publications.models import Publication, OccupationRepeatMode, OccupationRanges
from api.publications.serializers import OccupationRangeSerializer


def create_booking_occupation(data, publication_id):
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


def get_occupation_by_month(publication_id, year, month, day):
    occupations = OccupationRanges.objects.filter(related_publication=publication_id, start_date__year=year,
                                                  start_date__month=month)
    if day is not None:
        occupations = occupations.filter(start_date__day=day)
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


def __calculate_NO2(m):
    if m['valor'] < 54:
        return 0
    elif m['valor'] < 101:
        return 1
    elif m['valor'] < 361:
        return 2
    elif m['valor'] < 650:
        return 3
    elif m['valor'] < 1250:
        return 4
    else:
        return 5


def __calculate_PM10(m):
    if m['valor'] < 54:
        return 0
    elif m['valor'] < 155:
        return 1
    elif m['valor'] < 255:
        return 2
    elif m['valor'] < 355:
        return 3
    elif m['valor'] < 251:
        return 4
    else:
        return 5


def __calculate_O3(m):
    if m['valor'] < 60:
        return 0
    elif m['valor'] < 125:
        return 1
    elif m['valor'] < 165:
        return 2
    elif m['valor'] < 205:
        return 3
    elif m['valor'] < 405:
        return 4
    else:
        return 5


def get_contamination(latitude, longitude):
    return None
    try:
        response = requests.get(
            "http://10.4.41.47:6039/api/estaciones/?latitud=" + str(latitude) + "&longitud=" + str(longitude))
        if response.status_code == 200:
            resp = response.json()
            NO2 = 0
            PM10 = 0
            O3 = 0
            color_code = {
                0: "green",
                1: "yellow",
                2: "orange",
                3: "red",
                4: "purple",
                5: "maroon"
            }
            for m in resp['mediciones']:
                if m['contamintante'] == 'NO2':
                    NO2 = __calculate_NO2(m)
                elif m['contamintante'] == 'PM10':
                    PM10 = __calculate_PM10(m)
                elif m['contamintante'] == 'O3':
                    O3 = __calculate_O3(m)
            maximum = max(NO2, PM10, O3)
            return color_code[maximum]
        else:
            raise Exception("Error getting data from estacions API")
    except:
        print("Error getting contamination")
        return None




def __update_contamination():
    print("Updating contamination")
    publications = Publication.objects.all()
    for publication in publications:
        contamination = get_contamination(publication.localization.latitude,
                                                      publication.localization.longitude)
        if contamination is None:
            print("No connection with contamination API")
            return
        contamination_instance = Contamination.objects.filter(publication=publication).first()
        if contamination_instance is None:
            contamination_instance = Contamination(publication=publication, contamination=contamination)
            contamination_instance.save()
        else:
            contamination_instance.contamination = contamination
            contamination_instance.save()
    print("Contamination updated")


def sincronize_data_with_API_contamination():

    now_date = datetime.now() - timedelta(hours=1)
    fifteen_minutes_ago = now_date - timedelta(minutes=15)
    try:
        date_obj = Configs.objects.filter(key="last_date_contamination_checked")[0]
        last_date = datetime.strptime(date_obj.value, "%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        date_obj = Configs(key="last_date_contamination_checked", value=now_date)
        last_date = datetime(1970, 1, 1)

    if fifteen_minutes_ago > last_date:
        __update_contamination()
        date_obj.value = now_date
        date_obj.save()
