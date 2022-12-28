from rest_framework.response import Response
from rest_framework.views import APIView

from api.vehicles.models import CarsModel
from api.vehicles.services import get_data_vehicles


# Create your views here.
class VehiclesView(APIView):
    def get(self, request):
        get_data_vehicles()
        models = CarsModel.objects.all()
        # serialize models
        #print(data)

        return Response(models, status=200)
