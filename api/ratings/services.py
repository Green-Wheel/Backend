from datetime import datetime

from api.bookings.models import Bookings
from api.chargers.models import PublicChargers
from api.ratings.models import Ratings, PostRating, ClientsRating
from api.ratings.serializers import PostRatingSerializer, ClientsRatingSerializer, PublicPostRatingSerializer
from api.users.services import send_notification


def get_ratings_for_user(user_id):
    ratings = ClientsRating.objects.filter(user_id=user_id, active=True)
    return ratings


def get_ratings_from_publication(publication_id):
    ratings = PostRating.objects.filter(publication_id=publication_id, active=True)
    return ratings


def get_all_ratings():
    ratings = Ratings.objects.filter(active=True)
    return ratings

def get_rating(rating_id):
    return Ratings.objects.get(id=rating_id)

def send_new_post_rating_notification(rating):
    user = rating.publication.owner.id
    title = "New rating for your publication"
    body = "Your publication has been rated by a client"
    send_notification(user, title, body)

def send_new_client_rating_notification(rating):
    user = rating.client.id
    title = "New rating for your booking"
    body = "Your booking has been rated by the owner"
    send_notification(user, title, body)

def create_post_rating(rating):
    if rating.get("booking", None) is not None:
        booking = Bookings.objects.get(id=rating["booking"])
        if booking.user.id != rating["user"]:
            raise Exception("User is not client of the booking")
        if booking.end_date > datetime.now():
            raise Exception("Booking is not finished")
        serializer = PostRatingSerializer(data=rating)
    else:
        try:
            PublicChargers.objects.get(id=rating["publication"])
            serializer = PublicPostRatingSerializer(data=rating)
        except PublicChargers.DoesNotExist:
            serializer = PostRatingSerializer(data=rating)
            #raise Exception("The publication rated is not a public charger, it needs a booking id")

    if serializer.is_valid():
        serializer.save()
        new_rating = Ratings.objects.latest('id')
        send_new_post_rating_notification(new_rating)
        return new_rating
    else:
        raise Exception(serializer.errors)

def create_client_rating(rating):
    if rating.get("booking", None) is not None:
        booking = Bookings.objects.get(id=rating["booking"])
        if booking.publication.owner.id != rating["user"]:
            raise Exception("User is not owner of the publication")
        if booking.user.id != rating["client"]:
            raise Exception("Client is not client of the booking")
        if booking.end_date > datetime.now():
            raise Exception("Booking is not finished")
        serializer = ClientsRatingSerializer(data=rating)
    else:
        serializer = ClientsRatingSerializer(data=rating)
    if serializer.is_valid():
        serializer.save()
        new_rating = Ratings.objects.latest('id')
        send_new_client_rating_notification(new_rating)
        return new_rating
    else:
        raise Exception(serializer.errors)
