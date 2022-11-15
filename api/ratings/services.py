from api.ratings.models import Ratings
from api.ratings.serializers import RatingsSerializer


def get_ratings_for_user(user_id):
    ratings = Ratings.objects.filter(user_id=user_id)
    return RatingsSerializer(ratings,many=True).data

def get_ratings_for_publication(publication_id):
    ratings = Ratings.objects.filter(publication_id=publication_id)
    return RatingsSerializer(ratings,many=True).data

def get_all_ratings():
    ratings = Ratings.objects.all()
    return RatingsSerializer(ratings,many=True).data