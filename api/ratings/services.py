from datetime import datetime

from api.bookings.models import Bookings
from api.ratings.models import Ratings, PostRating, ClientsRating
from api.ratings.serializers import PostRatingSerializer, ClientsRatingSerializer


def get_ratings_for_user(user_id):
    ratings = ClientsRating.objects.filter(user_id=user_id)
    return ratings

def get_ratings_for_publication(publication_id):
    ratings = PostRating.objects.filter(publication_id=publication_id)
    return ratings

def get_all_ratings():
    ratings = Ratings.objects.all()
    return ratings

def create_post_rating(rating):
    booking = Bookings.objects.get(id=rating["booking"])
    if booking.user.id != rating["user"]:
        raise Exception("User is not client of the booking")
    if booking.end_date > datetime.now():
        raise Exception("Booking is not finished")
    serializer = PostRatingSerializer(data=rating)
    print(serializer)
    if serializer.is_valid():
        serializer.save()
        return Ratings.objects.latest('id')
    else:
        raise Exception(serializer.errors)

def create_client_rating(rating):
    booking = Bookings.objects.get(id=rating["booking"])
    if booking.publication.owner.id != rating["user"]:
        raise Exception("User is not owner of the publication")
    if booking.user.id != rating["client"]:
        raise Exception("Client is not client of the booking")
    if booking.end_date > datetime.now():
        raise Exception("Booking is not finished")
    serializer = ClientsRatingSerializer(data=rating)

    if serializer.is_valid():
        serializer.save()
        return Ratings.objects.latest('id')
    else:
        raise Exception(serializer.errors)