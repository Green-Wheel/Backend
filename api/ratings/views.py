from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RatingsSerializer
from .models import Ratings


# Create your views here.
class RatingsApiView(APIView):
    def get(self, request):
        rating_instance = Ratings.objects.all().filter()
        # rating_instance = Ratings.objects.filter(booking=1)
        # rating_instance = Ratings.objects.filter(booking=booking_id)
        serializer = RatingsSerializer(rating_instance, many=True)
        if not rating_instance:
            return Response(
                {"res": "Rating with the id doesn't exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(serializer.data, status=200)
