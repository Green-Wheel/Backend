from rest_framework.response import Response
from rest_framework.views import APIView

from api.vehicles.services import get_data_vehicles


# Create your views here.
class VehiclesView(APIView):
    def get(self, request):
        data = get_data_vehicles()
        print(data)
        return Response(data, status=200)
