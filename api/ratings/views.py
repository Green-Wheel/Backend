from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RatingsSerializer
from .models import Ratings
from .services import get_all_ratings


# Create your views here.
class RatingsApiView(APIView):
    def get(self, request):
        ratings = get_all_ratings()
        return Response(ratings, status=200)
